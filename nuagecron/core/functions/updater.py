from typing import Any
from nuagecron.core.adapters.base_database_adapter import BaseDBAdapter
from nuagecron.core.executors.base_executor import BaseExecutor

EXECUTOR_MAP = {cls.__name__: cls for cls in BaseExecutor.__subclasses__()}


def main(db_adapter: BaseDBAdapter, execution_id: str, update_payload: dict):
    execution = db_adapter.get_execution_by_id(execution_id)
    if execution:
        executor_cls = EXECUTOR_MAP[execution.executor]
        executor = executor_cls(execution)
        update = executor.process_update(update_payload)
        db_adapter.update_execution(
            execution.schedule_id, execution.execution_time, update
        )
