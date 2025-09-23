from fastapi import HTTPException
import boto3
from botocore.exceptions import ClientError
from app.services.s3.s3_setup import BUCKET_NAME, region

s3_client = boto3.client("s3", region_name=region)

def write_receipts(trade_id: str, receipt_file):
    key = f"trade_receipts/{trade_id}"
    try:
        response = s3_client.put_object(Bucket=BUCKET_NAME,
                                        Key=key,
                                        Body=receipt_file,
                                        ContentType="application/pdf")
        print(f"PutObject response: {response}")
    except ClientError as e:
        print(f"Failed to upload PDF to s3: {e}")
        raise HTTPException(status_code=500, detail="Upload failed")

def get_presigned_receipt_url(trade_id: str) -> str:
    key = f"trade_receipts/{trade_id}"
    try:
        presigned_url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': key
            },
            ExpiresIn=1800 # expire after 30 minutes
        )
        return presigned_url
    except ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            print("Receipt not found!")
        else:
            print(f"Error generating presigned URL: {e}")

def delete_receipt(receipt_key):
    try:
        response = s3_client.delete_object(Bucket=BUCKET_NAME, Key=receipt_key)
        print('DeleteObject response: ', response)
    except ClientError as e:
        print(e)
