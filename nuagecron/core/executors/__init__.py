from inspect import isclass
from typing import Dict, Type

from .base_executor import BaseExecutor


EXECUTOR_MAP: Dict[str, Type[BaseExecutor]] = {}


def register_executor(a_class):
    if not isclass(a_class) or not issubclass(a_class, BaseExecutor):
        raise ValueError(f"{a_class.__name__} is not an Executor")
    EXECUTOR_MAP[a_class.__name__] = a_class
