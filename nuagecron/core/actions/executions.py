from typing import Any, List, Optional

from nuagecron.core.models.executions import Execution


def create_execution(name: str, project_stack: Optional[str]) -> Execution:
    pass


def kill_execution(
    name: str, project_stack: Optional[str], execution_time: int
) -> bool:
    pass


def get_executions(
    name: str, project_stack: Optional[str], limit: int = 100
) -> List[Execution]:
    pass


def get_execution_by_id(execution_id: str) -> Execution:
    pass


def get_execution_by_name(
    name: str, project_stack: Optional[str], execution_time: int
) -> Execution:
    pass


def execute_with_overrides(name: str, project_stack: Optional[str], overrides: dict) -> Execution:
    pass