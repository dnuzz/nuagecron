from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from nuagecron.core.models.executions import Execution
from nuagecron.core.models.schedules import Schedule


class BaseDBAdapter(ABC):
    @abstractmethod
    def get_schedule(self, schedule_id: str) -> Optional[Schedule]:
        raise NotImplementedError()

    @abstractmethod
    def get_schedules_to_run(self, count: int = 100) -> List[Schedule]:
        raise NotImplementedError()

    @abstractmethod
    def get_schedules(self, start: str = None, count: int = 100) -> List[Schedule]:
        raise NotImplementedError()

    @abstractmethod
    def put_schedule(self, schedule: Schedule):
        raise NotImplementedError()

    @abstractmethod
    def get_schedule_set(self, project_stack: str) -> List[Schedule]:
        raise NotImplementedError()

    @abstractmethod
    def update_schedule(self, schedule_id: str, update: dict):
        raise NotImplementedError()

    @abstractmethod
    def delete_schedule(self, schedule_id: str):
        raise NotImplementedError()

    @abstractmethod
    def get_execution_by_id(self, execution_id: str) -> Optional[Execution]:
        raise NotImplementedError()

    @abstractmethod
    def get_execution(self, schedule_id: str, execution_time: int) -> Execution:
        raise NotImplementedError()

    @abstractmethod
    def get_executions(self, schedule_id: str, count: int = 100) -> List[Execution]:
        raise NotImplementedError()

    @abstractmethod
    def update_execution(self, schedule_id: str, execution_time: int, update: dict):
        raise NotImplementedError()

    @abstractmethod
    def put_execution(self, execution: Execution):
        raise NotImplementedError()
