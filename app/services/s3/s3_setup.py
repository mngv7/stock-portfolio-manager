import boto3
from botocore.exceptions import ClientError

BUCKET_NAME = "n11592931-receipts"
qut_username = "n11592931@qut.edu.au"
purpose = "assessment-2"
region = "ap-southeast-2"

s3_client = boto3.client("s3", region_name=region)

def create_receipts_bucket():
    try:
        s3_client.head_bucket(Bucket=BUCKET_NAME)
        print(f"Bucket '{BUCKET_NAME}' already exists.")
    except ClientError as e1:
        error_code = int(e1.response['Error']['Code'])
        if error_code == 404:
            try:
                response = s3_client.create_bucket(Bucket=BUCKET_NAME,
                                                   CreateBucketConfiguration={'LocationConstraint': region})
                print('Bucket created at:', response.get('Location'))
                tag_bucket()
            except Exception as e2:
                print(f"Failed to create bucket: {e2}")
        else:
            print(f"An error occured: {e1}")

def tag_bucket():
    try:
        response = s3_client.put_bucket_tagging(
            Bucket=BUCKET_NAME,
            Tagging={
                'TagSet': [
                    {'Key': 'qut-username', 'Value': qut_username},
                    {'Key': 'purpose', 'Value': purpose}
                ]
            }
        )
        print('Tagging response: ', response)
    except ClientError as e:
        print(e)

def delete_bucket():
    try:
        s3_client.delete_bucket(Bucket=BUCKET_NAME)
        print('Bucket deleted.')
    except ClientError as e:
        print(e)

if __name__ == "__main__":
    create_receipts_bucket()
