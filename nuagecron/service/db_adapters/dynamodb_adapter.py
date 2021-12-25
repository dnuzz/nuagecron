from typing import Any, List, Optional
from pydantic import BaseModel
from datetime import datetime
from pynamodb.models import Model
import boto3
from pynamodb.attributes import (
    DynamicMapAttribute,
    UTCDateTimeAttribute,
    UnicodeAttribute,
    NumberAttribute,
    JSONAttribute,
    BooleanAttribute,
    UnicodeSetAttribute,
)

from nuagecron.service.db_adapters.base_adapter import BaseDBAdapter
from nuagecron.domain.models.schedules import Schedule
from nuagecron.domain.models.executions import Execution


def type_to_dynamo_type(attribute: Any):
    if not attribute:
        return "NULL"
    if isinstance(attribute, float) or isinstance(attribute, int):
        return "N"
    if isinstance(attribute, str) or isinstance(attribute, datetime):
        return "S"
    if isinstance(attribute, dict):
        return "M"
    if isinstance(attribute, set):
        if isinstance(attribute[0], float) or isinstance(attribute[0], int):
            return "NS"
        elif isinstance(attribute[0], str):
            return "SS"
    if isinstance(attribute, bool):
        return "BOOL"
    if isinstance(attribute, list):
        return "L"
    raise ValueError(f"Could not coerce {attribute} to a DynamoDB type")


def dictionary_to_dynamo(a_dict: dict):
    dynamo_obj = {}
    for k, v in a_dict.items():
        ddb_type = type_to_dynamo_type(v)
        if ddb_type == "M":
            a_val = dictionary_to_dynamo(v)
        if ddb_type == "L":
            a_val = [{type_to_dynamo_type(x): x for x in a_val.items()}]
        else:
            a_val = v
        dynamo_obj[k] = {ddb_type: a_val}
    return dynamo_obj


def model_to_dynamo(model: BaseModel):
    return dictionary_to_dynamo(model.dict())


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


# Just ignore below here for now TODO


class ExecutionHistoryAttribute(UnicodeSetAttribute):
    def element_serialize(self, value: dict):
        """
        This serializes unicode / strings out as unicode strings.
        It does not touch the value if it is already a unicode str
        :param value:
        :return:
        """
        for k, v in value.items():
            return f"{k}:{v}"

    def element_deserialize(self, value: str):
        if value:
            value_parts = value.split(":")
            return {int(value_parts[0]): value_parts[1]}
        return None

    def serialize(self, value):
        if value is not None:
            if isinstance(value, dict):
                return [self.element_serialize({k: v}) for k, v in value.items()]
        return None

    def deserialize(self, value) -> dict:
        if value and len(value):
            ret_val: Dict[int, str] = {}  # type: Dict[str,str]
            for val in value:
                ret_val.update(self.element_deserialize(val))
            return ret_val
        return {}


class Schedule(Model):
    schedule_id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute(null=False)
    next_run = NumberAttribute(null=False)
    project_stack = UnicodeAttribute(null=False)
    payload = JSONAttribute(null=False)
    cron = UnicodeAttribute(null=False)
    executor = UnicodeAttribute(null=False)
    overrides_applied = BooleanAttribute(null=False, default=False)
    metadata = DynamicMapAttribute()
    execution_history = ExecutionHistoryAttribute()


class Execution(Model):
    class Meta:
        extra = "allow"

    schedule_id: str
    execution_time: int
    payload: dict
    invoke_time: Optional[datetime]
    update_time: Optional[datetime]
    execution_id: Optional[str]
    status: ExecutionStatus
