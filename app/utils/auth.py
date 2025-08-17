from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import datetime
from datetime import timezone
import jwt # type: ignore
from pydantic import BaseModel

SECRET_KEY = 'e9aae26be08551392be664d620fb422350a30349899fc254a0f37bfa1b945e36ff20d25b12025e1067f9b69e8b8f2ef0f767f6fff6279e5755668bf4bae88588'

security = HTTPBearer()

class AuthUser(BaseModel):
    username: str
    exp: int

def generate_access_token(username: str):
    payload = {
        'username': username,
        'exp': datetime.datetime.now(timezone.utc) + datetime.timedelta(minutes=30)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def authenticate_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> AuthUser:
    if not credentials or not credentials.scheme == 'Bearer':
        raise HTTPException(status_code=401, detail='Unauthorized')
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return AuthUser(**payload)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid token')