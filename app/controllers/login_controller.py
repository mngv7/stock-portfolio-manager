from fastapi import Request, HTTPException
from app.utils.auth import generate_access_token

users = {
    'ztaylor': {"password": "password"},
    'admin': {"password": "admin"}
}

async def login(request: Request):
    data = await request.json()
    username = data.get('username')
    password = data.get('password')
    user = users.get(username)
    
    if not user or user['password'] != password:
        raise HTTPException(status_code=401, detail='Unauthorized')
    
    token = generate_access_token(username)
    return {'authToken': token}
