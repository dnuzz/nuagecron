from .adapters import MockComputeAdapter, MockDatabaseAdapter
from nuagecron.core.functions.executor import main as executor_main
from nuagecron.core.functions.updater import main as updater_main
from nuagecron.core.functions.tick import main as tick_main
import pytest
from moto import mock_dynamodb
import boto3
import os

os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
os.environ["AWS_SECURITY_TOKEN"] = "testing"
os.environ["AWS_SESSION_TOKEN"] = "testing"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@mock_dynamodb
def test_tick():
    a = boto3.client("dynamodb")
    db_adapter = MockDatabaseAdapter()
    compute_adapter = MockComputeAdapter(db_adapter)
    tick_main(compute_adapter, db_adapter)
