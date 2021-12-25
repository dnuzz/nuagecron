from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from datetime import datetime
import boto3

from nuagecron.service.db_adapters.base_adapter import BaseDBAdapter
from nuagecron.domain.models.schedules import Schedule
from nuagecron.domain.models.executions import Execution

from dynamodb_json import json_util


def dictionary_to_dynamo(a_dict: dict):
    return json_util.dumps(a_dict, as_dict=True)


def model_to_dynamo(model: BaseModel):
    return dictionary_to_dynamo(model.dict())


def dynamo_to_dict(dynamo_object: dict):
    return json_util.loads(dynamo_object, as_dict=True)


class DynamoDbAdapter(BaseDBAdapter):
    def __init__(self):
        self.dynamodb_client = boto3.client("dynamodb")

    def _get_object(self, table: str, hash_key: Any, range_key: Any = None):
        self.dynamodb_client.get_item()

    def get_schedule(self, schedule_id: str) -> Schedule:
        raise NotImplementedError()

    def get_schedules_to_run(self) -> List[Schedule]:
        raise NotImplementedError()

    def put_schedule(self, schedule: Schedule):
        raise NotImplementedError()

    def update_schedule(self, schedule_id: str, update: dict):
        raise NotImplementedError()

    def delete_schedule(self, schedule_id: str):
        raise NotImplementedError()

    def get_execution_by_id(self, execution_id: str) -> Optional[Execution]:
        raise NotImplementedError()

    def get_execution(self, schedule_id: str, execution_time: int) -> Execution:
        raise NotImplementedError()

    def update_execution(self, schedule_id: str, execution_time: int, update: dict):
        raise NotImplementedError()

    def put_execution(self, execution: Execution):
        raise NotImplementedError()

    def delete_execution(self, execution: Execution):
        raise NotImplementedError()
