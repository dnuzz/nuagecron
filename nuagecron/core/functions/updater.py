from typing import Any
from nuagecron.core.adapters.base_database_adapter import BaseDBAdapter
from nuagecron.core.executors import BaseExecutor
from nuagecron.core.executors import EXECUTOR_MAP
from nuagecron.core.models.executions import ExecutionStatus


def main(db_adapter: BaseDBAdapter, execution_id: str, update_payload: dict):
    execution = db_adapter.get_execution_by_id(execution_id)
    if execution:
        executor_cls = EXECUTOR_MAP[execution.executor]
        executor = executor_cls(execution)
        update = executor.process_update(update_payload)
        db_adapter.update_execution(
            execution.schedule_id, execution.execution_time, update
        )
        if update.get('status'):
            schedule = db_adapter.get_schedule(execution.schedule_id)
            schedule.upsert_execution_history(execution.execution_time, update['status'])
            db_adapter.update_schedule(execution.schedule_id, {})