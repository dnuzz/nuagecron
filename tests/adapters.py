from typing import Optional
from nuagecron import SERVICE_NAME
from nuagecron.core.adapters.base_compute_adapter import BaseComputeAdapter
from nuagecron.adapters.aws.adapters import DynamoDbAdapter
from nuagecron.core.adapters.base_database_adapter import BaseDBAdapter
from nuagecron.core.functions.executor import main as executor_main
from nuagecron.core.functions.updater import main as updater_main
from nuagecron.core.functions.tick import main as tick_main
from moto import mock_dynamodb


@mock_dynamodb
class MockDatabaseAdapter(DynamoDbAdapter):
    def __init__(self):
        super().__init__()


class MockComputeAdapter(BaseComputeAdapter):
    def __init__(self, db_adapter: MockDatabaseAdapter):
        self.db_adapter = db_adapter

    def invoke_function(
        self, function_name: str, payload: dict, sync: bool = True, timeout: int = None
    ) -> dict:
        if function_name == f"{SERVICE_NAME}-executor":
            executor_main(
                self.db_adapter, payload["schedule_id"], payload["execution_time"]
            )
        if function_name == f"{SERVICE_NAME}-updater":
            updater_main(
                self.db_adapter,
                payload["execution_id"],
            )
        if function_name == f"{SERVICE_NAME}-tick":
            tick_main(self, self.db_adapter)
        return {}

    def invoke_container(
        self, container_name: str, payload: dict, timeout: int = None
    ) -> Optional[str]:
        return ""
