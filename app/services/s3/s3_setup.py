import boto3
from botocore.exceptions import ClientError

bucket_name = "n11592931-receipts"
qut_username = "n11592931@qut.edu.au"
purpose = "assessment-2"
region = "ap-southeast-2"

s3_client = boto3.client("s3", region_name=region)

def create_receipts_bucket():
    try:
        response = s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': region})
        print('Bucket created at:', response.get('Location'))
    except ClientError as e:
        print(e)

def tag_bucket():
    try:
        response = s3_client.put_bucket_tagging(
            Bucket=bucket_name,
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
        s3_client.delete_bucket(Bucket=bucket_name)
        print('Bucket deleted.')
    except ClientError as e:
        print(e)

if __name__ == "__main__":
    create_receipts_bucket()
    tag_bucket()
