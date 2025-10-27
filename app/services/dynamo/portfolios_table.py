import boto3
import aioboto3
from boto3.dynamodb.types import TypeDeserializer
from botocore.exceptions import ClientError
from app.services.dynamo.setup_tables import region, portfolios_table_name, qut_username
from app.models.portfolio_model import Portfolio
from app.utils.gen_id import generate_portfolio_id

session = aioboto3.Session()
deserializer = TypeDeserializer()

# First time initialization of a portfolio
def put_portfolio(user_uuid: str, portfolio_no: str):
    portfolio_id = generate_portfolio_id(user_uuid)
    try:
        dynamodb = boto3.client("dynamodb", region_name=region)
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

async def get_portfolio(portfolio_id: str):
    async with session.client("dynamodb", region_name=region) as dynamodb:
        try:
            response = await dynamodb.get_item(
                TableName=portfolios_table_name,
                Key={
                    "qut-username": {"S": qut_username},
                    "portfolio_id": {"S": portfolio_id}
                }
            )
            item = response.get("Item")
            return item
        except ClientError as e:
            print(f"Client error: {e}")
        except Exception as e:
            print(f"Exception: {e}")

async def load_portfolio_assets(portfolio: Portfolio):
    portfolio_id = generate_portfolio_id(portfolio.user_uuid)

    item = await get_portfolio(portfolio_id)
    
    if not item:
        portfolio.assets = {}
        return

    raw_assets = item.get("assets", {}).get("M", {})

    portfolio.assets = deserializer.deserialize({"M": raw_assets})
    portfolio.assets = {ticker: int(amount) for ticker, amount in portfolio.assets.items()}
