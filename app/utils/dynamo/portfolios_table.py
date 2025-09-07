import boto3
from botocore.exceptions import ClientError
from setup_tables import region, portfolios_table_name, qut_username
from app.models.portfolio_model import Portfolio

dynamodb = boto3.client("dynamodb", region_name=region)

def put_portfolio(portfolio: Portfolio):
    try:
        response = dynamodb.put_item(
            TableName=portfolios_table_name,
            Item={
                "qut-username": {"S": qut_username},
                "assets": {"M": portfolio.assets},
            },
            ConditionExpression="attribute_not_exists(email)"
        )
        print("PutItem response:", response)
    except ClientError as e:
        print(e)
