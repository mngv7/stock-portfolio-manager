import boto3
from botocore.exceptions import ClientError
from s3_setup import bucket_name, region

s3_client = boto3.client("s3", region_name=region)

def write_receipts(object_key, object_value):
    try:
        response = s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=object_value)
        print('PutObject response: ', response)
    except ClientError as e:
        print(e)

def read_receipts(receipt_key):
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=receipt_key)
        body = response['Body'].read().decode()
        print ('Object value: ', body)
    except ClientError as e:
        print(e)

def delete_receipt(receipt_key):
    try:
        response = s3_client.delete_object(Bucket=bucket_name, Key=receipt_key)
        print('DeleteObject response: ', response)
    except ClientError as e:
        print(e)
