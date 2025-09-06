import boto3
from botocore.exceptions import ClientError
from setup_tables import region, trades_table_name, qut_username
from app.models.trades_models import Trade
from app.models.users_models import User

dynamodb = boto3.client("dynamodb", region_name=region)

def put_trade(user: User, trade: Trade):
    sk_value = f"{user.email}#{trade.timestamp}"
    try:
        response = dynamodb.put_item(
            TableName=trades_table_name,
            Item={
                "qut-username": {"S": qut_username},
                "timestamp#email": {"S": sk_value},
                "email": {"S": user.email},
                "timestamp": {"S": trade.timestamp},
                "ticker": {"S": trade.ticker},
                "avg_price": {"S": trade.avg_price},
                "quantity": {"S": trade.quantity},
                "fee": {"S": trade.fee}
            },
            ConditionExpression="attribute_not_exists(email)"
        )
        print("PutItem response:", response)
    except ClientError as e:
        print(e)