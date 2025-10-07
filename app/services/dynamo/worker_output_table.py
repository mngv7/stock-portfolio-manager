import boto3
from boto3.dynamodb.types import TypeDeserializer
from botocore.exceptions import ClientError
from app.services.dynamo.setup_tables import region, qut_username

dynamodb = boto3.client("dynamodb", region_name=region)
deserializer = TypeDeserializer()

TABLE_NAME = "n11592931-worker-output"

def put_monte_carlo_result(user_uuid: str, result: dict):
    try:
        response = dynamodb.put_item(
            TableName=TABLE_NAME,
            Item={
                "qut-username": {"S": qut_username},
                "task-name": {"S": "monte_carlo"},
                "user_uuid": {"S": user_uuid},
                "result": {"M": result}
            }
        )
        print("PutItem response:", response)
    except ClientError as e:
        print("PutItem failed:", e)