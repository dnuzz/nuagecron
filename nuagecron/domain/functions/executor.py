from typing import Any

from nuagecron.domain.adapters.utils import get_db_adapter
from nuagecron.domain.executors.base_executor import BaseExecutor

EXECUTOR_MAP = {cls.__name__: cls for cls in BaseExecutor.__subclasses__()}


def main(schedule_id: str, execution_time: int):
    db_adapter = get_db_adapter()
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
