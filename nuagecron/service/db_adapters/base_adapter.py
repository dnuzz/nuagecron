from abc import ABC, abstractmethod
from typing import List

from nuagecron.domain.models.schedules import Schedule
from nuagecron.domain.models.executions import Execution


class BaseDBAdapter(ABC):
    @abstractmethod
    def get_schedule(self, schedule_id: str) -> Schedule:
        raise NotImplementedError()

    @abstractmethod
    def get_schedules_to_run(self) -> List[Schedule]:
        raise NotImplementedError()

    @abstractmethod
    def put_schedule(self, schedule: Schedule):
        raise NotImplementedError()

    @abstractmethod
    def update_schedule(self, schedule_id: str, update: dict):
        raise NotImplementedError()

    @abstractmethod
    def delete_schedule(self, schedule_id: str):
        raise NotImplementedError()

    @abstractmethod
    def get_execution_by_id(self, execution_id: str) -> Execution:
        raise NotImplementedError()

    @abstractmethod
    def get_execution(self, schedule_id: str, execution_time: int) -> Execution:
        raise NotImplementedError()

    @abstractmethod
    def update_execution(self, schedule_id: str, execution_time: int, update: dict):
        raise NotImplementedError()

    @abstractmethod
    def put_execution(self, execution: Execution):
        raise NotImplementedError()

    @abstractmethod
    def delete_execution(self, execution: Execution):
        raise NotImplementedError()
