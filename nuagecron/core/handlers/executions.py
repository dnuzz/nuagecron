from typing import Any, List, Optional
from nuagecron.core.adapters.base_compute_adapter import BaseComputeAdapter
from nuagecron.core.adapters.base_database_adapter import BaseDBAdapter

from nuagecron.core.models.executions import Execution


class ExecutionHandler:
    def __init__(
        self, db_adapter: BaseDBAdapter, compute_adapter: BaseComputeAdapter
    ) -> None:
        self.compute_adapter = compute_adapter
        self.db_adapter = db_adapter

    def create_execution(self, name: str, project_stack: Optional[str]) -> Execution:
        pass

    def kill_execution(
        self, name: str, project_stack: Optional[str], execution_time: int
    ) -> bool:
        pass

    def get_executions(
        self, name: str, project_stack: Optional[str], limit: int = 100
    ) -> List[Execution]:
        pass

    def get_execution_by_id(self, execution_id: str) -> Execution:
        pass

    def get_execution_by_name(
        self, name: str, project_stack: Optional[str], execution_time: int
    ) -> Execution:
        pass

    def create_execution(
        self, name: str, project_stack: Optional[str], overrides: Optional[dict]
    ) -> Execution:
        pass
