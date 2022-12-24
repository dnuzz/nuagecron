from typing import Any

from nuagecron.core.functions.executor import main as executor_main
from nuagecron.core.functions.updater import main as updater_main
from nuagecron.core.functions.tick import main as tick_main

from .adapters import AWSComputeAdapter, DynamoDbAdapter

db_adapter = DynamoDbAdapter()
compute_adapter = AWSComputeAdapter()


def executor_lambda_handler(payload: Any, context: Any):
    schedule_id: str = payload["schedule_id"]
    execution_time: int = int(payload["execution_time"])
    executor_main(db_adapter, schedule_id, execution_time)


def tick_lambda_handler(payload: Any, Context: Any):
    tick_main(compute_adapter, db_adapter)


def _get_execution_id(payload: dict) -> str:
    # This should take the payload and parse out the `batch_id` or request_id or whatever would come from the SNS notification that would ID the execution
    raise NotImplementedError()


def updater_lambda_handler(payload: dict, context: dict):
    execution_id = _get_execution_id(payload)
    updater_main(db_adapter, execution_id, payload)
