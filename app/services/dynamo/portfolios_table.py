import boto3
from botocore.exceptions import ClientError
from setup_tables import region, portfolios_table_name, qut_username
from app.models.portfolio_model import Portfolio

dynamodb = boto3.client("dynamodb", region_name=region)

# First time initialization of a portfolio
def put_portfolio(user_uuid: str, portfolio_no: str):
    portfolio_id = f"{user_uuid}#{portfolio_no}"
    try:
        response = dynamodb.put_item(
            TableName=portfolios_table_name,
            Item={
                "qut-username": {"S": qut_username},
                "portfolio_id": {"S": portfolio_id},
                "user_uuid": {"S": user_uuid},
                "assets": {"M": {}}
            },
            ConditionExpression="attribute_not_exists(portfolio_id)"
        )
        print("PutItem response:", response)
    except ClientError as e:
        print("PutItem failed:", e)

