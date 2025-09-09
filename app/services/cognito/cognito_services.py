import boto3
from dotenv import load_dotenv
import os
import hmac, hashlib, base64 

load_dotenv()

client_id = os.getenv("USERS_COGNITO_CLIENT_ID")
client_secret = os.getenv("USERS_COGNITO_CLIENT_SECRET")

def secretHash(clientId, clientSecret, username):
    message = bytes(username + clientId,'utf-8') 
    key = bytes(clientSecret,'utf-8') 
    return base64.b64encode(hmac.new(key, message, digestmod=hashlib.sha256).digest()).decode() 

def signup(username: str, email: str, password: str):
    client = boto3.client("cognito-idp", region_name="ap-southeast-2")
    try:
        response = client.sign_up(
            ClientId=client_id,
            Username=username,
            Password=password,
            SecretHash=secretHash(client_id, client_secret, username),
            UserAttributes=[{"Name": "email", "Value": email}]
        )
        return response
    except Exception as e:
        print(f"Error during sign-up: {e}")
        return None
    
def authenticate(username: str, password: str):
    client = boto3.client("cognito-idp", region_name="ap-southeast-2")
    try:
        response = client.initiate_auth(
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": username,
                "PASSWORD": password,
                "SECRET_HASH": secretHash(client_id, client_secret, username)
            },
            ClientId=client_id  # match signUp.py
        )
        tokens = response["AuthenticationResult"]
        # Optionally verify tokens here using jose or cognito public keys
        return tokens
    except Exception as e:
        print(f"Error during authentication: {e}")
        return None

def confirm(username: str, confirmation_code: str):
    client = boto3.client("cognito-idp", region_name="ap-southeast-2")
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
