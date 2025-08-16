from fastapi import Request, HTTPException
from app.utils.auth import generate_access_token
from app.models.users_models import User 
from app.utils.users import users

async def login(request: Request):
    data = await request.json()
    username = data.get('username')
    password = data.get('password')
    user = users.get(username)
    
    if not user or user.password != password:
        raise HTTPException(status_code=401, detail='Unauthorized')
    
    token = generate_access_token(username)
    return {'authToken': token}
