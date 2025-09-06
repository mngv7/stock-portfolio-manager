import boto3
from botocore.exceptions import ClientError

qut_username = "n11592931@qut.edu.au"
region = "ap-southeast-2"
users_table_name = "n11592931-users"
portfolios_table_name = "n11592931-portfolios"
trades_table_name = "n11592931-trades"

dynamodb = boto3.client("dynamodb", region_name=region)

def create_table_users():
    try:
        response = dynamodb.create_table(
            TableName=users_table_name,
            AttributeDefinitions=[
                {"AttributeName": "qut-username", "AttributeType": "S"},
                {"AttributeName": "email", "AttributeType": "S"},
            ],
            KeySchema=[
                {"AttributeName": "qut-username", "KeyType": "HASH"},
                {"AttributeName": "email", "KeyType": "RANGE"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )
        print("Create Table response:", response) 
    except ClientError as e:
        print(e)
