import boto3
from botocore.exceptions import ClientError

qut_username = "n11592931@qut.edu.au"
region = "ap-southeast-2"
users_table_name = "n11592931-users"
portfolios_table_name = "n11592931-portfolios"
trades_table_name = "n11592931-trades"

dynamodb = boto3.client("dynamodb", region_name=region)

def create_users_table():
    existing_tables = dynamodb.list_tables()['TableNames']
    if users_table_name in existing_tables:
        print(f"Table '{users_table_name}' already exists.")
        return

    try:
        response = dynamodb.create_table(
            TableName=users_table_name,
            AttributeDefinitions=[
                {"AttributeName": "qut-username", "AttributeType": "S"},
                {"AttributeName": "uuid", "AttributeType": "S"},
            ],
            KeySchema=[
                {"AttributeName": "qut-username", "KeyType": "HASH"},
                {"AttributeName": "uuid", "KeyType": "RANGE"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )
        print("Create Table response:", response) 
    except ClientError as e:
        print(e)

def create_portfolios_table():
    existing_tables = dynamodb.list_tables()['TableNames']
    if portfolios_table_name in existing_tables:
        print(f"Table '{portfolios_table_name}' already exists.")
        return

    try:
        response = dynamodb.create_table(
            TableName=portfolios_table_name,
            AttributeDefinitions=[
                {"AttributeName": "qut-username", "AttributeType": "S"},
                {"AttributeName": "portfolio_id", "AttributeType": "S"},
            ],
            KeySchema=[
                {"AttributeName": "qut-username", "KeyType": "HASH"},
                {"AttributeName": "portfolio_id", "KeyType": "RANGE"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )
        print("Create Table response:", response) 
    except ClientError as e:
        print(e)

def create_trades_table():
    existing_tables = dynamodb.list_tables()['TableNames']
    if trades_table_name in existing_tables:
        print(f"Table '{trades_table_name}' already exists.")
        return

    try:
        response = dynamodb.create_table(
            TableName=trades_table_name,
            AttributeDefinitions=[
                {"AttributeName": "qut-username", "AttributeType": "S"},
                {"AttributeName": "trade_id", "AttributeType": "S"},
            ],
            KeySchema=[
                {"AttributeName": "qut-username", "KeyType": "HASH"},
                {"AttributeName": "trade_id", "KeyType": "RANGE"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )
        print("Create Table response:", response) 
    except ClientError as e:
        print(e)

if __name__ == "__main__":
    create_users_table()
    create_portfolios_table()
    create_trades_table()
