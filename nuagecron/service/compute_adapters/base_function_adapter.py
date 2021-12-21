from abc import ABC, abstractclassmethod
from typing import Optional


class BaseComputeAdapter(ABC):
    @abstractclassmethod
    def invoke_function(
        self, function_name: str, payload: dict, sync: bool = True, timeout: int = None
    ) -> Optional[str]:
        raise NotImplementedError()

    @abstractclassmethod
    def invoke_container(
        self, container_name: str, payload: dict, sync: bool = True, timeout: int = None
    ) -> Optional[str]:
        raise NotImplementedError()
