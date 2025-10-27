from fastapi import APIRouter, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from app.services.cognito import cognito_services as cognito
from app.services.cognito.cognito_services import verify_jwt
from app.services.dynamo.users_table import put_user
from app.services.dynamo.portfolios_table import put_portfolio
import jwt

router = APIRouter()

class GroupUpdate(BaseModel):
    group: str

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

@router.post("/api/v2/auth")
def check_jwt(user = Depends(verify_jwt)):
    return user["sub"]

@router.get("/api/v1/jwt/decode")
def decode_jwt(user = Depends(verify_jwt)):
    return user

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

@router.patch("/api/v1/user/group")
def update_user_group(data: GroupUpdate, user=Depends(verify_jwt)):
    username = user["cognito:username"]
    new_group = cognito.update_user_group(username, data.group)
    return {"username": username, "new_group": new_group}

origins = ["*"]

app = FastAPI(
    title="Authentication worker",
    description="Handles authentication as a microservice",
    version="0.0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.include_router(router)
