import boto3
from botocore.exceptions import ClientError
from setup_tables import region, trades_table_name, qut_username
from app.models.trades_models import Trade
from app.models.users_models import User

dynamodb = boto3.client("dynamodb", region_name=region)

def put_trade(user_uuid: str, trade: Trade):
    trade_id = f"{user_uuid}#{trade.timestamp}"
    try:
        response = dynamodb.put_item(
            TableName=trades_table_name,
            Item={
                "qut-username": {"S": qut_username},
                "trade_id": {"S": trade_id},
                "timestamp": {"S": trade.timestamp},
                "ticker": {"S": trade.ticker},
                "avg_price": {"N": str(trade.avg_price)},
                "quantity": {"N": str(trade.quantity)},
                "fee": {"N": str(trade.fee)},
            },
            ConditionExpression="attribute_not_exists(trade_id)"
        )
        print("PutItem response:", response)
    except ClientError as e:
        print("PutItem failed:", e)