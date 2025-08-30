from fastapi import APIRouter, Depends
from app.utils.auth import authenticate_token
router = APIRouter()

@router.post('/api/v1/auth')
def check_jwt(user = Depends(authenticate_token)):
    return {"user": user}
