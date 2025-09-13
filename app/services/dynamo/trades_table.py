import boto3
from botocore.exceptions import ClientError
from app.services.dynamo.setup_tables import region, trades_table_name, qut_username, portfolios_table_name
from app.models.trades_models import Trade
from app.models.portfolio_model import Portfolio

dynamodb = boto3.client("dynamodb", region_name=region)

def load_trades(portfolio: Portfolio):
    portfolio_id_prefix = f"{portfolio.user_uuid}#{portfolio.portfolio_no}"

    try:
        response = dynamodb.query(
            TableName=trades_table_name,
            KeyConditionExpression="#username = :pk AND begins_with(trade_id, :prefix)",
            ExpressionAttributeNames={
                "#username": "qut-username"
            },
            ExpressionAttributeValues={
                ":pk": {"S": qut_username},
                ":prefix": {"S": portfolio_id_prefix}
            },
            ScanIndexForward=True
        )

        items = response.get("Items", [])

        # clear existing trades
        portfolio.trades = {}

        for item in items:
            trade = Trade(
                ticker=item["ticker"]["S"],
                avg_price=float(item["avg_price"]["N"]),
                quantity=float(item["quantity"]["N"]),
                fee=float(item["fee"]["N"]),
                timestamp=item["timestamp"]["N"]
            )

            # group trades by ticker
            if trade.ticker not in portfolio.trades:
                portfolio.trades[trade.ticker] = []
            portfolio.trades[trade.ticker].append(trade)

    except ClientError as e:
        print(f"Failed to load trades for portfolio {portfolio.portfolio_no}: {e}")
        portfolio.trades = {}

def log_trade_transaction(user_uuid: str, portfolio_no: str, trade: Trade, assets: dict):
    """
    Atomically logs a trade and updates portfolio assets using DynamoDB transaction.
    """

    trade_id = f"{user_uuid}#{trade.timestamp}"
    portfolio_id = f"{user_uuid}#{portfolio_no}"

    # Convert assets dict to DynamoDB format
    dynamo_assets = {ticker: {"N": str(qty)} for ticker, qty in assets.items()}

    print(dynamo_assets)

    try:
        response = dynamodb.transact_write_items(
            TransactItems=[
                {
                    "Put": {
                        "TableName": trades_table_name,
                        "Item": {
                            "qut-username": {"S": qut_username},
                            "trade_id": {"S": trade_id},
                            "timestamp": {"N": str(trade.timestamp)},
                            "ticker": {"S": trade.ticker},
                            "avg_price": {"N": str(trade.avg_price)},
                            "quantity": {"N": str(trade.quantity)},
                            "fee": {"N": str(trade.fee)}
                        },
                        "ConditionExpression": "attribute_not_exists(trade_id)"
                    }
                },
                {
                    "Update": {
                        "TableName": portfolios_table_name,
                        "Key": {
                            "qut-username": {"S": qut_username},
                            "portfolio_id": {"S": portfolio_id}
                        },
                        "UpdateExpression": "SET assets = :assets",
                        "ExpressionAttributeValues": {
                            ":assets": {"M": dynamo_assets}
                        }
                    }
                }
            ]
        )
        print("Transaction successful:", response)

    except ClientError as e:
        print(f"Transaction failed: {e}")
        raise