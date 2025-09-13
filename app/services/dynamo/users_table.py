import boto3
from botocore.exceptions import ClientError
from app.services.dynamo.setup_tables import region, users_table_name, qut_username

dynamodb = boto3.client("dynamodb", region_name=region)

def put_user(email: str, username: str, user_uuid: str):
    try:
        response = dynamodb.put_item(
            TableName=users_table_name,
            Item={
                "qut-username": {"S": qut_username},
                "user_uuid": {"S": user_uuid},
                "email": {"S": email},
                "username": {"S": username}
            },
            ConditionExpression="attribute_not_exists(user_uuid)"
        )
        print("PutItem response:", response)
    except ClientError as e:
        print(e)

