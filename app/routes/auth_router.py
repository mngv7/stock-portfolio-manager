from fastapi import APIRouter, Depends
from app.utils.auth import authenticate_token
router = APIRouter()

@router.post('/auth')
def check_jwt(user = Depends(authenticate_token)):
    return {"user": user}
