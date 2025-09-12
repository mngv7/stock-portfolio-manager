import json
import boto3
from botocore.exceptions import ClientError

secret_name = "n11592931-cognito-secrets"
region_name = "ap-southeast-2"

def get_secret():
    client = boto3.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response.get('SecretString')
        secret_dict = json.loads(secret)
        return secret_dict
    except ClientError as e:
        print(e)