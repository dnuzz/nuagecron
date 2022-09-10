from datetime import datetime
from typing import Any, List, Optional
from nuagecron.core.adapters.base_compute_adapter import BaseComputeAdapter
from nuagecron.core.adapters.base_database_adapter import BaseDBAdapter

from nuagecron.core.models.executions import Execution, ExecutionStatus
from nuagecron.core.executors import EXECUTOR_MAP
from nuagecron.core.models.utils import get_schedule_id
from nuagecron import SERVICE_NAME

# TODO This may not even be needed or should maybe live in the api layer
class ExecutionHandler:
    def __init__(
        self, db_adapter: BaseDBAdapter, compute_adapter: BaseComputeAdapter
    ) -> None:
        self.compute_adapter = compute_adapter
        self.db_adapter = db_adapter

    def kill_execution(self, execution_id: str) -> bool:
        execution = self.db_adapter.get_execution_by_id(execution_id)
        executor_class = EXECUTOR_MAP[execution.executor]
        executor = executor_class(execution)
        killed = executor.try_kill()
        if killed:
            self.db_adapter.update_execution(
                execution.schedule_id,
                execution.execution_time,
                {"status": ExecutionStatus.killed},
            )
        return killed

    def list_executions(
        self, name: str, project_stack: Optional[str], limit: int = 100
    ) -> List[Execution]:
        schedule_id = get_schedule_id(name, project_stack)
        return self.db_adapter.get_executions(schedule_id, limit)

    def get_execution(
        self, name: str, project_stack: Optional[str], execution_time: int
    ) -> Execution:
        schedule_id = get_schedule_id(name, project_stack)
        return self.db_adapter.get_execution(schedule_id, execution_time)

    def create_execution(
        self, name: str, project_stack: Optional[str], overrides: Optional[dict] = None
    ) -> Execution:
        schedule_id = get_schedule_id(name, project_stack)
        schedule = self.db_adapter.get_schedule(schedule_id)
        schedule_as_dict = schedule.dict()
        if overrides:
            schedule_as_dict.update(overrides)
        schedule_as_dict["execution_time"] = int(datetime.utcnow().timestamp())
        schedule_as_dict["status"] = ExecutionStatus.ready
        new_execution = Execution(**schedule_as_dict)
        self.db_adapter.put_execution(new_execution)
        self.compute_adapter.invoke_function(
            f"{SERVICE_NAME}-executor",
            {
                "schedule_id": schedule_id,
                "execution_time": schedule_as_dict["execution_time"],
            },
            sync=False,
        )
        return new_execution
