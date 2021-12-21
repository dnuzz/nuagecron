from nuagecron.service.db_adapters.base_adapter import BaseDBAdapter
from nuagecron.service.db_adapters.dynamodb_adapter import DynamoDbAdapter
from nuagecron.service.compute_adapters.aws_compute_adapter import BaseComputeAdapter
from nuagecron.service.compute_adapters.aws_compute_adapter import AWSComputeAdapter
import boto3


def get_compute_adapter() -> BaseComputeAdapter:
    return AWSComputeAdapter()

def get_db_adapter() -> BaseDBAdapter:
    return DynamoDbAdapter()