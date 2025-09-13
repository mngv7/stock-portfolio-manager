from fastapi import APIRouter, Depends, Header, HTTPException
import app.controllers.auth_controller as auth
from pydantic import BaseModel, EmailStr
import app.services.cognito.cognito_services as cognito
from app.services.cognito.cognito_services import verify_jwt
from app.services.dynamo.users_table import put_user
from app.services.dynamo.portfolios_table import put_portfolio
import jwt

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    phoneNumber: str

class ConfirmEmailRequest(BaseModel):
    username: str
    confirmationCode: str

class ChallengeResponse(BaseModel):
    username: str
    authCode: str
    session: str

@router.post('/api/v1/auth')
def check_jwt(user = Depends(verify_jwt)):
    return user

@router.post("/api/v2/auth")
def check_jwt(user = Depends(verify_jwt)):
    return user

@router.post("/api/v1/login")
async def login(request: LoginRequest):
    return await auth.login(request.username, request.password)

@router.post("/api/v2/login")
def login(request: LoginRequest):
    return cognito.authenticate(request.username, request.password)

@router.post("/api/v1/challenge_response")
def challenge_response(request: ChallengeResponse):
    challenge_response = cognito.email_otp_challenge(request.username, request.authCode, request.session)
    auth_result = challenge_response.get("AuthenticationResult")

    if auth_result:
        id_token = auth_result.get("IdToken")
        decoded_token = jwt.decode(id_token, options={"verify_signature": False})
        email = decoded_token.get("email")
        user_uuid = decoded_token["sub"]
        put_user(email, request.username, user_uuid)
        put_portfolio(user_uuid, 1) # Create user's first portfolio
        return {"id_token": id_token}

    return {"error": "Challenge not completed"}

@router.post("/api/v1/signup")
def signup(request: SignupRequest):
    return cognito.signup(request.username, request.email, request.password, request.phoneNumber)

@router.post("/api/v1/confirm_email")
def confirm_email(request: ConfirmEmailRequest):
    return cognito.confirm(request.username, request.confirmationCode)
