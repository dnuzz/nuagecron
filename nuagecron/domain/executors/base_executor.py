from abc import ABC, abstractmethod
from typing import Tuple
from pydantic import BaseModel
from nuagecron.domain.models.executions import Execution, ExecutionStatus


class BaseExecutor(ABC, BaseModel):
    class PayloadValidation(ABC, BaseModel):
        pass

    def __init__(self, execution: Execution):
        self.execution: Execution = execution
        self.payload: dict = self.PayloadValidation(**self.execution.payload).dict()

    """
    This should validate the params to the best of it's ability using the payload
    """

    @abstractmethod
    def validate(self):
        raise NotImplementedError()

    """
    This should prepare variables for runtime
    """

    @abstractmethod
    def prepare(self):
        raise NotImplementedError()

    """
    This should set the invoke_time and the execution_id on the execution object
    """

    @abstractmethod
    def execute(
        self,
    ) -> Tuple[
        str, ExecutionStatus
    ]:  # This should set the invoke time and the execution_id
        raise NotImplementedError()

    """
    When an update is passed to this it should update the execution and the update_time attributes
    """

    @abstractmethod
    def process_update(self, update: dict):
        raise NotImplementedError()

    """
    This should attempt to kill the running execution and return whether that was successful or not
    """

    @abstractmethod
    def try_kill(self) -> bool:
        raise NotImplementedError()
