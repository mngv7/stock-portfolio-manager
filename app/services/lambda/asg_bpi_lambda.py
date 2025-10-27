import boto3
import json

sqs = boto3.client('sqs')
cloudwatch = boto3.client('cloudwatch')
autoscaling = boto3.client('autoscaling')

QUEUE_URL = 'https://sqs.ap-southeast-2.amazonaws.com/901444280953/n11592931-monte-carlo-tasks'
ASG_NAME = 'n11592931-monte-carlo-scaler'
METRIC_NAMESPACE = 'StockPortfolioManager/SQSBacklog'
METRIC_NAME = 'BacklogPerInstance'

def lambda_handler(event, context):
    # Get queue length
    sqs_response = sqs.get_queue_attributes(
        QueueUrl = QUEUE_URL,
        AttributeNames=['ApproximateNumberOfMessages']
    )

    queue_length = int(sqs_response['Attributes'].get('ApproximateNumberOfMessages', 0))

    # Get ASG instance count
    asg_response = autoscaling.describe_auto_scaling_groups(AutoScalingGroupNames=[ASG_NAME])
    instance_count = len(asg_response['AutoScalingGroups'][0]['Instances'])
    instance_count = max(1, instance_count)

    # backlog per instance
    bpi = queue_length / instance_count

    cloudwatch.put_metric_data(
        Namespace=METRIC_NAMESPACE,
        MetricData=[{
            'MetricName': METRIC_NAME,
            'Value': bpi,
            'Unit': 'Count',
            'Dimensions': [
                {
                    'Name': 'AutoScalingGroupName',
                    'Value': ASG_NAME
                }
            ]
        }]
    )

    print(f"Published BPI: {bpi} (Queue: {queue_length}, Instances: {instance_count})")
    return {'statusCode': 200}