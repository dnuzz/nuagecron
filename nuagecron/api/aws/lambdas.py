from typing import Any

from nuagecron.core.functions.executor import main as executor_main
from typing import Any
from nuagecron.core.functions.updater import main as updater_main

from nuagecron.core.functions.tick import main as tick_main


def executor_lambda_handler(payload: Any, context: Any):
    schedule_id: str = payload["schedule_id"]
    execution_time: int = payload["execution_time"]
    executor_main(schedule_id, execution_time)


def tick_lambda_handler(payload: Any, Context: Any):
    tick_main()


def _get_execution_id(payload: dict) -> str:
    raise NotImplementedError()


def updater_lambda_handler(payload: dict, context: dict):
    execution_id = _get_execution_id(payload)
    updater_main(execution_id, payload)
