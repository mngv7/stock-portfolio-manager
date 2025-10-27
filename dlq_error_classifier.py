from app.services.dynamo.portfolios_table import get_portfolio, load_portfolio_assets
from app.models.portfolio_model import Portfolio
from app.services.s3.dlq_messages_bucket import write_message
import yfinance as yf
import json
import asyncio
import aioboto3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SQS_QUEUE_URL = "https://sqs.ap-southeast-2.amazonaws.com/901444280953/n11592931-monte-carlo-tasks-dlq"
REGION_NAME = "ap-southeast-2"


def do_tickers_exist(tickers: list[str]) -> bool:
    """Check if all given tickers exist on Yahoo Finance."""
    for ticker_str in tickers:
        ticker = yf.Ticker(ticker_str)
        try:
            info = ticker.info
            if not info:
                return False
        except Exception:
            return False
    return True


async def dlq_error_classifier():
    session = aioboto3.Session()

    async with session.client("sqs", region_name=REGION_NAME) as sqs_client:
        while True:
            try:
                response = await sqs_client.receive_message(
                    QueueUrl=SQS_QUEUE_URL,
                    MaxNumberOfMessages=1,
                    WaitTimeSeconds=15,
                    VisibilityTimeout=300,
                )

                messages = response.get("Messages", [])
                if not messages:
                    continue

                for message in messages:
                    logger.info(f"Message received: {message}")
                    body = message.get("Body", "{}")

                    try:
                        task = json.loads(body)
                    except Exception as e:
                        logger.error(f"Invalid JSON: {e}")
                        await write_message(body, "invalid_json")
                        await sqs_client.delete_message(
                            QueueUrl=SQS_QUEUE_URL,
                            ReceiptHandle=message["ReceiptHandle"],
                        )
                        continue

                    uuid = task.get("user")
                    portfolio_id = task.get("portfolio")

                    if not uuid:
                        await write_message(task, "missing_keys")
                    elif not portfolio_id:
                        await write_message(task, "missing_keys", uuid)
                    elif task.get("type") != "monte_carlo":
                        await write_message(task, "unknown_task", uuid)
                    elif not get_portfolio(portfolio_id):
                        await write_message(task, "unknown_portfolio", uuid)
                    else:
                        try:
                            portfolio = Portfolio(uuid, portfolio_id)
                            await load_portfolio_assets(portfolio)
                            tickers = list(portfolio.assets.keys())

                            if not do_tickers_exist(tickers):
                                await write_message(task, "unknown_ticker", uuid)
                            else:
                                await write_message(task, "other", uuid)
                        except Exception as e:
                            logger.error(f"Portfolio load error for {uuid}: {e}")
                            await write_message(task, "other", uuid)

                    await sqs_client.delete_message(
                        QueueUrl=SQS_QUEUE_URL,
                        ReceiptHandle=message["ReceiptHandle"],
                    )

            except Exception as e:
                logger.error(f"Error in worker loop: {e}")
                await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(dlq_error_classifier())
