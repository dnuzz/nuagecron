from nuagecron.core.adapters.aws_adapters import AWSComputeAdapter, DynamoDbAdapter
from nuagecron.core.adapters.base_compute_adapter import BaseComputeAdapter
from nuagecron.core.adapters.base_database_adapter import BaseDBAdapter


def get_compute_adapter() -> BaseComputeAdapter:
    return AWSComputeAdapter()


def get_db_adapter() -> BaseDBAdapter:
    return DynamoDbAdapter()
