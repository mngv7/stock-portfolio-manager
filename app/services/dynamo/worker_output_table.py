import boto3
import aioboto3
from boto3.dynamodb.types import TypeDeserializer
from botocore.exceptions import ClientError
from app.services.dynamo.setup_tables import region, qut_username

session = aioboto3.Session()
deserializer = TypeDeserializer()
TABLE_NAME = "n11592931-worker-output"

async def put_monte_carlo_result(user_uuid: str, result: dict):
    async with session.client("dynamodb", region_name=region) as dynamodb:
        try:
            response = await dynamodb.put_item(
                TableName=TABLE_NAME,
                Item={
                    "qut-username": {"S": qut_username},
                    "user-uuid": {"S": user_uuid},
                    "task_name": {"S": "monte_carlo"},
                    "result": {"M": result}
                }
            )
            print("PutItem response:", response)
        except ClientError as e:
            print("PutItem failed:", e)
        except Exception as e:
            print(f"Exception: {e}")

def get_monte_carlo_result(user_uuid: str):
    dynamodb = boto3.client("dynamodb", region_name=region)
    try:
        response = dynamodb.get_item(
            TableName = TABLE_NAME,
            Key={
                "qut-username": {"S": qut_username},
                "user-uuid": {"S": user_uuid}
            }
        )
        return response
    except ClientError as e:
        print("Get item failed:", e)