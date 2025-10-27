import asyncio
import json
import aioboto3
import logging
from app.services.dynamo.worker_output_table import put_monte_carlo_result
from app.services.dynamo.portfolios_table import load_portfolio_assets
from app.models.portfolio_model import Portfolio
import app.utils.dynamo_formatter as dynamo_formatter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SQS_QUEUE_URL = "https://sqs.ap-southeast-2.amazonaws.com/901444280953/n11592931-monte-carlo-tasks"
REGION_NAME = "ap-southeast-2"

async def monte_carlo_worker():
    session = aioboto3.Session()
    async with session.client("sqs", region_name=REGION_NAME) as sqs_client:
        while True:
            try:
                response = await sqs_client.receive_message(
                    QueueUrl=SQS_QUEUE_URL,
                    MaxNumberOfMessages=1,
                    WaitTimeSeconds=15,
                    VisibilityTimeout=300
                )

                logger.info("Receiving message")

                messages = response.get("Messages", [])
                if not messages:
                    continue

                for message in messages:
                    logger.info(f"Message received: {message}")
                    try:
                        task = json.loads(message['Body'])
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse message body: {e}")
                        # Don't delete the message, let it retry for eventual DLQ
                        # await sqs_client.delete_message(
                        #     QueueUrl=SQS_QUEUE_URL,
                        #     ReceiptHandle=message["ReceiptHandle"]
                        # )
                        continue

                    if task.get("task") == "monte_carlo":
                        logger.info("Monte carlo task detected!")
                        user_uuid = task.get("user")
                        if user_uuid:
                            try:
                                portfolio = Portfolio(user_uuid, "1")
                                await load_portfolio_assets(portfolio)
                                logger.info("Calculating forecast...")
                                result = portfolio.monte_carlo_forecast()
                                logger.info("Putting results...")
                                await put_monte_carlo_result(user_uuid, dynamo_formatter.str_int_flat_dict(result))
                            except Exception as e:
                                logger.error(f"Error processing Monte Carlo task for user {user_uuid}: {e}")
                                continue

                    logger.info("Deleting message...")
                    await sqs_client.delete_message(
                        QueueUrl=SQS_QUEUE_URL,
                        ReceiptHandle=message["ReceiptHandle"]
                    )
            except Exception as e:
                logger.error(f"Error in worker loop: {e}")
                await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(monte_carlo_worker())