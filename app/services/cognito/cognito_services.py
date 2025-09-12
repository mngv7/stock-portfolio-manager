import boto3
from dotenv import load_dotenv
import os
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import requests
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
import hmac, hashlib, base64 
from pathlib import Path

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

client_id = os.getenv("USERS_COGNITO_CLIENT_ID")
client_secret = os.getenv("USERS_COGNITO_CLIENT_SECRET")
user_pool_id = os.getenv("USERS_POOL_ID")

security = HTTPBearer()

region = "ap-southeast-2"

JWKS_URL = f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json"
JWKS = requests.get(JWKS_URL).json()

def secretHash(clientId, clientSecret, username):
    message = bytes(username + clientId,'utf-8') 
    key = bytes(clientSecret,'utf-8') 
    return base64.b64encode(hmac.new(key, message, digestmod=hashlib.sha256).digest()).decode() 

def signup(username: str, email: str, password: str, phone_number: str):
    client = boto3.client("cognito-idp", region_name=region)
    try:
        response = client.sign_up(
            ClientId=client_id,
            Username=username,
            Password=password,
            SecretHash=secretHash(client_id, client_secret, username),
            UserAttributes=[
                {"Name": "email", "Value": email}]
        )
        return response
    except Exception as e:
        print(f"Error during sign-up: {e}")
        return None

def authenticate(username: str, password: str):
    client = boto3.client("cognito-idp", region_name=region)
    try:
        response = client.initiate_auth(
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": username,
                "PASSWORD": password,
                "SECRET_HASH": secretHash(client_id, client_secret, username)
            },
            ClientId=client_id
        )
        return response
    except Exception as e:
        print(f"Error during authentication: {e}")
        return None

def email_otp_challenge(username: str, auth_code: str, session: str):
    client = boto3.client("cognito-idp", region_name=region)
    try:
        response = client.respond_to_auth_challenge(
            ClientId=client_id,
            ChallengeName="EMAIL_OTP",
            Session=session,
            ChallengeResponses={
                'USERNAME': username,
                'EMAIL_OTP_CODE': auth_code,  # must match the challenge
                'SECRET_HASH': secretHash(client_id, client_secret, username)
            }
        )
        return response
    except Exception as e:
        print(f"Error during MFA authentication: {e}")

def confirm(username: str, confirmation_code: str):
    client = boto3.client("cognito-idp", region_name=region)
    try:
        response = client.confirm_sign_up(
            ClientId=client_id,
            Username=username,
            ConfirmationCode=confirmation_code,
            SecretHash=secretHash(client_id, client_secret, username)
        )
        return response
    except Exception as e:
        print(f"Error during confirmation: {e}")
        return None
    
def verify_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials or credentials.scheme != "Bearer":
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            JWKS,
            algorithms=["RS256"],
            audience=client_id,
            issuer=f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}"
        )
        return {"sub": payload["sub"]}
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
