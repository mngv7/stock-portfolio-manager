import boto3
from botocore.exceptions import ClientError

ssm = boto3.client("ssm", region_name="ap-southeast-2")

parameters_cache = {}

def fetch_parameter_aws(parameter_name: str) -> str | None:
    try:
        response = ssm.get_parameter(Name=parameter_name)
        return response["Parameter"]["Value"]
    except ClientError:
        return None

def fetch_parameter_local(parameter_name: str) -> str | None:
    if parameter_name in parameters_cache:
        return parameters_cache[parameter_name]

    value = fetch_parameter_aws(parameter_name)
    if value is not None:
        parameters_cache[parameter_name] = value
    return value
