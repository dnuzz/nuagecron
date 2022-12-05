from importlib import import_module
from inspect import isclass
from pathlib import Path
from pkgutil import iter_modules
from abc import ABC, abstractmethod
from typing import Dict, Tuple, Optional, Type

from pydantic import BaseModel
from .base_executor import BaseExecutor

from nuagecron.core.models.executions import Execution, ExecutionStatus

# A bit of copy/pasta to automatically import all files in this subdirectory.
# This automatically resolves all subcalsses of BaseExecutor


# class BaseExecutor(ABC):

#     execution: Execution
#     payload: dict

#     class PayloadValidation(BaseModel):
#         pass

#     def __init__(self, execution: Execution):
#         self.execution: Execution = execution
#         self.payload: dict = self.PayloadValidation(**self.execution.payload).dict()

#     @abstractmethod
#     def validate(self):

#         """
#         This should validate the params to the best of it's ability using the payload
#         """
#         raise NotImplementedError()

#     @abstractmethod
#     def prepare(self):
#         """
#         This should prepare variables for runtime and store within the executor instance for the execute call
#         """
#         raise NotImplementedError()

#     @abstractmethod
#     def execute(
#         self,
#     ) -> Tuple[Optional[str], ExecutionStatus]:
#         """
#         This should execute the contents and return both an execution status and any attribute updates that need to be performed
#         """
#         raise NotImplementedError()

#     @abstractmethod
#     def process_update(self, update: dict) -> dict:
#         """
#         This should take in an update dictionary from a source specific to this executor
#         and return a dictionary that represents the new/ updated attributes for the execution
#         """
#         raise NotImplementedError()

#     @abstractmethod
#     def try_kill(self) -> bool:
#         """
#         This should attempt to kill the running execution and return whether that was successful or not
#         """
#         raise NotImplementedError()


EXECUTOR_MAP: Dict[str, Type[BaseExecutor]] = {}


def register_executor(a_class):
    if not isclass(a_class) or not issubclass(a_class, BaseExecutor):
        raise ValueError(f"{a_class.__name__} is not an Executor")
    EXECUTOR_MAP[a_class.__name__] = a_class


from .lambda_executor import LambdaExecutor
