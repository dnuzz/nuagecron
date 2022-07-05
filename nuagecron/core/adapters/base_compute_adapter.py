from abc import ABC, abstractmethod
from typing import Optional


class BaseComputeAdapter(ABC):
    @abstractmethod
    def invoke_function(
        self, function_name: str, payload: dict, sync: bool = True, timeout: int = None
    ) -> dict:
        raise NotImplementedError()

    @abstractmethod
    def invoke_container(
        self, container_name: str, payload: dict, timeout: int = None
    ) -> Optional[str]:
        raise NotImplementedError()
