from collections import defaultdict
from datetime import datetime
from typing import Dict, Optional, List, Tuple
from uuid import uuid4
from nuagecron.core.executors import BaseExecutor
from nuagecron.core.executors import register_executor
from nuagecron.core.models.executions import Execution, ExecutionStatus

from nuagecron.core.models.schedules import Schedule
from nuagecron import SERVICE_NAME
from nuagecron.core.adapters.base_compute_adapter import BaseComputeAdapter
from nuagecron.core.adapters.base_database_adapter import BaseDBAdapter
from nuagecron.core.functions.executor import main as executor_main
from nuagecron.core.functions.updater import main as updater_main
from nuagecron.core.functions.tick import main as tick_main


class MockDatabaseAdapter(BaseDBAdapter):
    def __init__(self):
        self.schedules: Dict[str, Schedule] = {}
        self.executions: Dict[str, Dict[int, Execution]] = defaultdict(dict)
        self.executions_by_id: Dict[str, Execution] = {}
        self.schedules_set: Dict[str, List[str]] = defaultdict(list)

    def get_schedule(self, schedule_id: str) -> Optional[Schedule]:
        return self.schedules.get(schedule_id)

    def get_schedules_to_run(self, count: int = 100) -> List[Schedule]:
        schedules = self.schedules.values()
        ret_val = list(
            filter(lambda x: x.next_run < datetime.utcnow().timestamp(), schedules)
        )
        return ret_val[:count]

    def put_schedule(self, schedule: Schedule):
        self.schedules[schedule.schedule_id] = schedule

    def get_schedule_set(self, project_stack: str) -> List[Schedule]:
        stack_schedule_ids = self.schedules_set[project_stack]
        a_set = [self.schedules[x] for x in stack_schedule_ids]
        return a_set

    def update_schedule(self, schedule_id: str, update: dict):
        for k, v in update.items():
            self.schedules[schedule_id].__setattr__(k, v)

    def delete_schedule(self, schedule_id: str):
        self.schedules.pop(schedule_id, None)

    def get_execution_by_id(self, execution_id: str) -> Optional[Execution]:
        return self.executions_by_id.get(execution_id)

    def get_execution(self, schedule_id: str, execution_time: int) -> Execution:
        return self.executions[schedule_id][execution_time]

    def get_executions(self, schedule_id: str, count: int = 100) -> List[Execution]:
        executions = self.executions[schedule_id]
        ret_val: List[Execution] = []
        for v in executions.values():
            if len(ret_val) == count:
                return ret_val
            ret_val.append(v)
        return ret_val

    def update_execution(self, schedule_id: str, execution_time: int, update: dict):
        execution = self.executions[schedule_id][execution_time]
        for k, v in update.items():
            execution.__setattr__(k, v)

    def put_execution(self, execution: Execution):
        self.executions[execution.schedule_id][execution.execution_time] = execution
        if execution.execution_id:
            self.executions_by_id[execution.execution_id] = execution

    def open_transaction(self):
        pass

    def commit_transaction(self):
        pass

    def rollback_transaction(self):
        pass


class MockComputeAdapter(BaseComputeAdapter):
    def __init__(self, db_adapter: MockDatabaseAdapter):
        self.db_adapter = db_adapter

    def invoke_function(
        self, function_name: str, payload: dict, sync: bool = True, timeout: int = None
    ) -> dict:
        if function_name == f"{SERVICE_NAME}-executor":
            executor_main(
                self.db_adapter, payload["schedule_id"], payload["execution_time"]
            )
        if function_name == f"{SERVICE_NAME}-updater":
            updater_main(
                self.db_adapter,
                payload["execution_id"],
            )
        if function_name == f"{SERVICE_NAME}-tick":
            tick_main(self, self.db_adapter)
        return {}

    def invoke_container(
        self, container_name: str, payload: dict, timeout: int = None
    ) -> Optional[str]:
        return ""


@register_executor
class MockExecutor(BaseExecutor):
    class PayloadValidation(BaseExecutor.PayloadValidation):
        a: str

    def validate(self):

        """
        This should validate the params to the best of it's ability using the payload
        """
        pass

    def prepare(self):
        """
        This should prepare variables for runtime and store within the executor instance for the execute call
        """
        pass

    def execute(
        self,
    ) -> Tuple[Optional[str], ExecutionStatus]:
        """
        This should execute the contents and return both an execution status and any attribute updates that need to be performed
        """
        return str(uuid4()), ExecutionStatus.running

    def process_update(self, update: dict) -> dict:
        """
        This should take in an update dictionary from a source specific to this executor
        and return a dictionary that represents the new/ updated attributes for the execution
        """
        return update

    def try_kill(self) -> bool:
        """
        This should attempt to kill the running execution and return whether that was successful or not
        """
        return True
