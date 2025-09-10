from fastapi import APIRouter, Depends, Header, HTTPException
import app.controllers.auth_controller as auth
from pydantic import BaseModel, EmailStr
import app.services.cognito.cognito_services as cognito
from app.services.cognito.cognito_services import verify_jwt

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class ConfirmEmailRequest(BaseModel):
    username: str
    code: str

@router.post('/api/v1/auth')
def check_jwt(user = Depends(verify_jwt)):
    return user

@router.post("/api/v2/auth")
def check_jwt(authorization: str = Header(...)):
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid auth scheme")
    return cognito.verify_jwt(token)

@router.post("/api/v1/login")
async def login(request: LoginRequest):
    return await auth.login(request.username, request.password)

@router.post("/api/v2/login")
async def login(request: LoginRequest):
    return cognito.authenticate(request.username, request.password)

@router.post("/api/v1/signup")
def signup(request: SignupRequest):
    return cognito.signup(request.username, request.email, request.password)

@router.post("/api/v1/confirm_email")
def confirm_email(request: ConfirmEmailRequest):
    return cognito.confirm(request.username, request.code)
