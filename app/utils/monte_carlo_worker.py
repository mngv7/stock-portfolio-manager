import asyncio
import json
import aioboto3
from app.services.dynamo.worker_output_table import put_monte_carlo_result
from app.services.dynamo.portfolios_table import load_portfolio_assets
from app.models.portfolio_model import Portfolio

SQS_QUEUE_URL = "https://sqs.ap-southeast-2.amazonaws.com/901444280953/n11592931-monte-carlo-tasks"
REGION_NAME = "ap-southeast-2"

async def monte_carlo_worker():
    session = aioboto3.Session()
    async with session.client("sqs", region_name=REGION_NAME) as sqs_client:
        while True:
            response = await sqs_client.receive_message(
                QueueUrl=SQS_QUEUE_URL,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=15,
                VisibilityTimeout=300  # adjust based on processing time
            )
            print("Receiving message")

            messages = response.get("Messages", [])
            
            if not messages:
                continue

            for message in messages:
                print(f"Message received: {message}")
                task = json.loads(message['Body'])

                if task.get("type") == "monte_carlo":
                    print("Monte carlo task detected!")
                    user_uuid = task.get("user")
                
                    if user_uuid:
                        portfolio = Portfolio(user_uuid, "1")
                        load_portfolio_assets(portfolio)
                        print("Calculating forecast...")
                        result = portfolio.monte_carlo_forecast()
                        print("Putting results...")
                        put_monte_carlo_result(user_uuid, result)
                
                print("Deleting message...")
                # Delete message
                await sqs_client.delete_message(
                    QueueUrl=SQS_QUEUE_URL,
                    ReceiptHandle=message["ReceiptHandle"]
                )

if __name__ == "__main__":
    asyncio.run(monte_carlo_worker())
