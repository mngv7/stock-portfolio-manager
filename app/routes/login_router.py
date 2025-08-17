from fastapi import APIRouter, Request
import app.controllers.login_controller as lc
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(request: LoginRequest):
    return await lc.login(request.username, request.password)
