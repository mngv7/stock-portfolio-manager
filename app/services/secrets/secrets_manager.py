import boto3
from botocore.exceptions import ClientError


def get_secret():
    secret_name = "n11592931-cognito-secrets"
    region_name = "ap-southeast-2"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']
    print(secret)