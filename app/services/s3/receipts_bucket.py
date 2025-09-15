from fastapi import HTTPException
import boto3
from botocore.exceptions import ClientError
from app.services.s3.s3_setup import bucket_name, region

s3_client = boto3.client("s3", region_name=region)

def write_receipts(trade_id: str, receipt_file):
    try:
        response = s3_client.put_object(Bucket=bucket_name,
                                        Key=f"trade_receipts/{trade_id}",
                                        Body=receipt_file,
                                        ContentType="application/pdf")
        print(f"PutObject response: {response}")
    except ClientError as e:
        print(f"Failed to upload PDF to s3: {e}")
        raise HTTPException(status_code=500, detail="Upload failed")

def get_receipt(trade_id: str):
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=trade_id)
        body = response['Body'].read().decode()
        print('Object value: ', body)
    except ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            print("Receipt not found!")
        else:
            print(f"Get receipt error occured: {e}")

def delete_receipt(receipt_key):
    try:
        response = s3_client.delete_object(Bucket=bucket_name, Key=receipt_key)
        print('DeleteObject response: ', response)
    except ClientError as e:
        print(e)
