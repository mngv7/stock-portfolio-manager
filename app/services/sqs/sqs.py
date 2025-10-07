import json
import aioboto3

SQS_QUEUE_URL = "https://sqs.ap-southeast-2.amazonaws.com/901444280953/n11592931-assessment-3"
REGION_NAME = "ap-southeast-2"

async def send_message(message: dict):
    session = aioboto3.Session()
    async with session.client("sqs", region_name=REGION_NAME) as sqs_client:
        send_response = await sqs_client.send_message(
            QueueUrl=SQS_QUEUE_URL,
            DelaySeconds=10,
            MessageBody=json.dumps(message)
        )
        return send_response
