import json
import aioboto3
from botocore.exceptions import ClientError
from datetime import date, datetime

session = aioboto3.Session()
BUCKET_NAME = "n11592931-dlq-messages"
REGION = "ap-southeast-2"

async def write_message(message: dict, error_class: str, uuid: str = "unknown_user"):
    async with session.client("s3", region_name=REGION) as s3_client:
        timestamp = datetime.now().strftime("%H%M%S")
        key = f"{error_class}/{date.today()}/message_{timestamp}_{uuid}.json"

        try:
            response = await s3_client.put_object(Bucket=BUCKET_NAME,
                                            Key=key,
                                            Body=json.dumps(message))
            print(f"PutObject response: {response}")
        except ClientError as e:
            print(f"Failed to upload DLQ message to s3: {e}")
