from typing import Any

from nuagecron.core.adapters.utils import get_db_adapter
from nuagecron.core.executors.base_executor import BaseExecutor

EXECUTOR_MAP = {cls.__name__: cls for cls in BaseExecutor.__subclasses__()}


def main(execution_id: str, update_payload: dict):
    db_adapter = get_db_adapter()
    execution = db_adapter.get_execution_by_id(execution_id)
    if execution:
        executor_cls = EXECUTOR_MAP[execution.executor]
        executor = executor_cls(execution)
        update = executor.process_update(update_payload)
        db_adapter.update_execution(
            execution.schedule_id, execution.execution_time, update
        )
