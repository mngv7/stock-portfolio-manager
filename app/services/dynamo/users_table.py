import boto3
from botocore.exceptions import ClientError
from app.services.dynamo.setup_tables import region, users_table_name, qut_username
from app.models.users_models import User

dynamodb = boto3.client("dynamodb", region_name=region)

def put_user(email: str, username: str, uuid: str):
    try:
        response = dynamodb.put_item(
            TableName=users_table_name,
            Item={
                "qut-username": {"S": qut_username},
                "email": {"S": email},
                "username": {"S": username},
                "uuid": {"S": uuid},
            },
            ConditionExpression="attribute_not_exists(email)"
        )
        print("PutItem response:", response)
    except ClientError as e:
        print(e)

