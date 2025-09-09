from fastapi import APIRouter, Depends
from app.utils.auth import authenticate_token
import app.controllers.auth_controller as auth
from pydantic import BaseModel, EmailStr
import app.services.cognito.cognito_services as cognito

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
def check_jwt(user = Depends(authenticate_token)):
    return {"user": user}

@router.post("/api/v1/login")
async def login(request: LoginRequest):
    return await auth.login(request.username, request.password)

@router.post("/api/v1/signup")
def signup(request: SignupRequest):
    return cognito.signup(request.username, request.email, request.password)

@router.post("/api/v1/confirm_email")
def confirm_email(request: ConfirmEmailRequest):
    return cognito.confirm(request.username, request.code)
