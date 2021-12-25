from typing import Any
from nuagecron.service.lambdas.utils import get_db_adapter
from nuagecron.domain.executors.base_executor import BaseExecutor

EXECUTOR_MAP = {cls.__name__: cls for cls in BaseExecutor.__subclasses__()}


def _get_execution_id(payload: dict) -> str:
    raise NotImplementedError()


def lambda_handler(payload: dict, context: dict):
    db_adapter = get_db_adapter()
    execution_id = _get_execution_id(payload)
    execution = db_adapter.get_execution_by_id(execution_id)
    if execution:
        executor_cls = EXECUTOR_MAP[execution.executor]
        executor = executor_cls(execution)
        update = executor.process_update(payload)
        db_adapter.update_execution(
            execution.schedule_id, execution.execution_time, update
        )
