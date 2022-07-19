from typing import Any

from nuagecron.core.adapters.base_database_adapter import BaseDBAdapter
from nuagecron.core.executors import EXECUTOR_MAP


def main(db_adapter: BaseDBAdapter, schedule_id: str, execution_time: int):
    execution = db_adapter.get_execution(schedule_id, execution_time)
    executor_class = EXECUTOR_MAP[execution.executor]
    executor = executor_class(execution)
    executor.prepare()
    execution_id, status = executor.execute()
    execution.execution_id = execution_id
    execution.status = status
    db_adapter.update_execution(
        schedule_id, execution_time, {"execution_id": execution_id, "status": status}
    )
    # TODO update the exection_history in the schedule object
