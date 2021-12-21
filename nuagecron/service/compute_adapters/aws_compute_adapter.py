from typing import Optional
from nuagecron.service.compute_adapters.base_compute_adapter import BaseComputeAdapter


class AWSComputeAdapter(BaseComputeAdapter):
    def __init__(self) -> None:
        super().__init__()

    def invoke_function(
        self, function_name: str, payload: dict, sync: bool = True, timeout: int = None
    ) -> Optional[str]:
        raise NotImplementedError()

    def invoke_container(
        self, container_name: str, payload: dict, sync: bool = True, timeout: int = None
    ) -> Optional[str]:
        raise NotImplementedError()
