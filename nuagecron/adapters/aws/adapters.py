from datetime import datetime
import json
from typing import List, Optional, Tuple

import boto3
from dynamodb_json import json_util
from pydantic import BaseModel

from nuagecron import SERVICE_NAME
from nuagecron.core.adapters.base_compute_adapter import BaseComputeAdapter
from nuagecron.core.adapters.base_database_adapter import BaseDBAdapter
from nuagecron.core.models.executions import Execution
from nuagecron.core.models.schedules import Schedule


def dictionary_to_dynamo(a_dict: dict, as_update=False) -> dict:
    def add_update_param(attr: dict):
        for k in attr.keys():
            primary_key = list(attr[k].keys())[0]
            new_val = {"Value": {primary_key: None}, "Action": "PUT"}
            # if primary_key == "M":
            #    add_update_param(attr[k][primary_key])
            new_val["Value"][primary_key] = attr[k][primary_key]
            attr[k] = new_val

    ret_val: dict = json_util.dumps(a_dict, as_dict=True)
    if as_update:
        add_update_param(ret_val)

    return ret_val


def model_to_dynamo(model: BaseModel):
    model_as_dict = model.dict(exclude_none=True)
    if isinstance(model, Schedule):
        if model_as_dict["enabled"]:
            model_as_dict["enabled"] = "TRUE"
        else:
            model_as_dict["enabled"] = "FALSE"
    return dictionary_to_dynamo(model_as_dict)


def dynamo_to_dict(dynamo_object: dict):
    return json_util.loads(dynamo_object, as_dict=True)


SCHEDULE_TABLE_NAME = f"{SERVICE_NAME}-schedules"
EXECUTION_TABLE_NAME = f"{SERVICE_NAME}-executions"


class DynamoDbAdapter(BaseDBAdapter):
    def __init__(self):
        super().__init__()
        self.dynamodb_client = boto3.client("dynamodb")

    def get_schedule(self, schedule_id: str) -> Optional[Schedule]:
        payload = self.dynamodb_client.get_item(
            TableName=SCHEDULE_TABLE_NAME, Key={"schedule_id": {"S": schedule_id}}
        )
        if "Item" in payload:
            return Schedule(**dynamo_to_dict(payload["Item"]))
        return None

    def get_schedules_to_run(self, count: int = 100) -> List[Schedule]:
        response = self.dynamodb_client.query(
            TableName=SCHEDULE_TABLE_NAME,
            IndexName=f"{SCHEDULE_TABLE_NAME}-enabled",
            KeyConditionExpression="enabled = :T AND next_run < :CT",
            ExpressionAttributeValues={
                ":T": {"S": "TRUE"},
                ":CT": {"N": str(int(datetime.utcnow().timestamp()))},
            },
            Limit=count,
            ScanIndexForward=False,
        )
        ret_val = [Schedule(**dynamo_to_dict(item)) for item in response["Items"]]
        if len(ret_val) >= count:
            return ret_val
        while "LastEvaluatedKey" in response:
            response = self.dynamodb_client.query(
                TableName=SCHEDULE_TABLE_NAME,
                IndexName=f"{SCHEDULE_TABLE_NAME}-enabled",
                KeyConditionExpression="enabled = :T",
                ExpressionAttributeValues={
                    ":T": {"S": "TRUE"},
                    ":CT": {"N": str(int(datetime.utcnow().timestamp()))},
                },
                Limit=count,
                ScanIndexForward=False,
                ExclusiveStartKey=response["LastEvaluatedKey"],
            )
            ret_val.extend(
                [Schedule(**dynamo_to_dict(item)) for item in response["Items"]]
            )
            if len(ret_val) >= count:
                return ret_val
        return ret_val

    def get_schedules(
        self, start: str = None, count: int = 100
    ) -> Tuple[List[Schedule], Optional[str]]:
        if start:
            addl_kwargs = {"ExclusiveStartKey": {"schedule_id": {"S": start}}}
        else:
            addl_kwargs = {}
        response = self.dynamodb_client.scan(
            TableName=SCHEDULE_TABLE_NAME, Limit=count, **addl_kwargs
        )
        ret_val = [Schedule(**dynamo_to_dict(item)) for item in response["Items"]]
        if len(ret_val) >= count:
            return ret_val, None
        while "LastEvaluatedKey" in response:
            response = self.dynamodb_client.scan(
                TableName=SCHEDULE_TABLE_NAME,
                Limit=count,
                ExclusiveStartKey=response["LastEvaluatedKey"],
            )
            ret_val.extend(
                [Schedule(**dynamo_to_dict(item)) for item in response["Items"]]
            )
            if len(ret_val) >= count:
                return ret_val, response["LastEvaluatedKey"]
        return ret_val, response.get("LastEvaluatedKey")

    def put_schedule(self, schedule: Schedule):
        self.dynamodb_client.put_item(
            TableName=SCHEDULE_TABLE_NAME, Item=model_to_dynamo(schedule)
        )

    def update_schedule(self, schedule_id: str, update: dict):
        attr_updates = dictionary_to_dynamo(update, as_update=True)
        if "enabled" in update:
            if update["enabled"]:
                attr_updates["enabled"] = {"S": "TRUE", "Action": "PUT"}
            else:
                attr_updates["enabled"] = {"S": "FALSE", "Action": "PUT"}
        self.dynamodb_client.update_item(
            TableName=SCHEDULE_TABLE_NAME,
            Key={"schedule_id": {"S": schedule_id}},
            AttributeUpdates=dictionary_to_dynamo(update, as_update=True),
        )

    def delete_schedule(self, schedule_id: str):
        self.dynamodb_client.delete_item(
            TableName=SCHEDULE_TABLE_NAME, Key={"schedule_id": {"S": schedule_id}}
        )

    def get_execution_by_id(self, execution_id: str) -> Optional[Execution]:
        response = self.dynamodb_client.query(
            TableName=EXECUTION_TABLE_NAME,
            IndexName=f"{EXECUTION_TABLE_NAME}-execution-id",
            Select="ALL_ATTRIBUTES",
            KeyConditionExpression="execution_id = :V",
            ExpressionAttributeValues={":V": {"S": execution_id}},
        )
        items = response["Items"]
        if items.__len__() == 0:
            return None
        if items.__len__() > 1:
            print(
                f"Warning: query returned more than one execution for execution_id: {execution_id}"
            )
        return Execution(**items[0])

    def get_execution(self, schedule_id: str, execution_time: int) -> Execution:
        payload = self.dynamodb_client.get_item(
            TableName=EXECUTION_TABLE_NAME,
            Key={
                "schedule_id": {"S": schedule_id},
                "execution_time": {"N": str(execution_time)},
            },
        )
        if not payload:
            raise ValueError(
                f"There was no execution for schedule_id:{schedule_id}, execution_time:{execution_time}"
            )
        return Execution(**dynamo_to_dict(payload["Item"]))

    def get_executions(
        self, schedule_id: str, count: int = 25, start: str = None
    ) -> Tuple[List[Execution], Optional[str]]:
        if start:
            addl_kwargs = {"ExclusiveStartKey": {"schedule_id": {"S": start}}}
        else:
            addl_kwargs = {}
        response = self.dynamodb_client.query(
            TableName=EXECUTION_TABLE_NAME,
            Limit=count,
            KeyConditionExpression="schedule_id = :V",
            ExpressionAttributeValues={":V": {"S": schedule_id}},
            ScanIndexForward=False,
            **addl_kwargs,
        )
        ret_val = [Execution(**dynamo_to_dict(item)) for item in response["Items"]]
        if len(ret_val) >= count:
            return ret_val, None
        while "LastEvaluatedKey" in response:
            response = self.dynamodb_client.query(
                TableName=EXECUTION_TABLE_NAME,
                Limit=count,
                KeyConditionExpression="schedule_id = :V",
                ExpressionAttributeValues={":V": {"S": schedule_id}},
                ScanIndexForward=False,
                ExclusiveStartKey=response["LastEvaluatedKey"],
            )
            ret_val.extend(
                [Execution(**dynamo_to_dict(item)) for item in response["Items"]]
            )
            if len(ret_val) >= count:
                return ret_val, response["LastEvaluatedKey"]
        return ret_val, response.get("LastEvaluatedKey")

    def update_execution(self, schedule_id: str, execution_time: int, update: dict):
        self.dynamodb_client.update_item(
            TableName=EXECUTION_TABLE_NAME,
            Key={
                "schedule_id": {"S": schedule_id},
                "execution_time": {"N": str(execution_time)},
            },
            AttributeUpdates=dictionary_to_dynamo(update, as_update=True),
        )

    def put_execution(self, execution: Execution):
        self.dynamodb_client.put_item(
            TableName=EXECUTION_TABLE_NAME, Item=model_to_dynamo(execution)
        )

    def get_schedule_set(self, project_stack: str) -> List[Schedule]:
        response = self.dynamodb_client.query(
            TableName=SCHEDULE_TABLE_NAME,
            IndexName=f"{SCHEDULE_TABLE_NAME}-project-stack",
            KeyConditionExpression="project_stack = :V",
            ExpressionAttributeValues={":V": {"S": project_stack}},
            Limit=100,
            ScanIndexForward=False,
        )
        ret_val = [Schedule(**dynamo_to_dict(item)) for item in response["Items"]]
        while "LastEvaluatedKey" in response:
            response = self.dynamodb_client.query(
                TableName=SCHEDULE_TABLE_NAME,
                IndexName=f"{SCHEDULE_TABLE_NAME}-project-stack",
                KeyConditionExpression="project_stack = :V",
                ExpressionAttributeValues={":V": {"S": project_stack}},
                Limit=100,
                ScanIndexForward=False,
                ExclusiveStartKey=response["LastEvaluatedKey"],
            )
            ret_val.extend(
                [Schedule(**dynamo_to_dict(item)) for item in response["Items"]]
            )
        return ret_val


class AWSComputeAdapter(BaseComputeAdapter):
    def __init__(self) -> None:
        super().__init__()
        self.lambda_client = boto3.client("lambda")

    def invoke_function(
        self, function_name: str, payload: dict, sync: bool = True, timeout: int = None
    ) -> dict:
        payload_str = str.encode(json.dumps(payload, default=str))
        if sync:
            invoke_type = "RequestResponse"
        else:
            invoke_type = "Event"
        response = self.lambda_client.invoke(
            FunctionName=function_name,
            Payload=payload_str,
            InvocationType=invoke_type,
            LogType="Tail",
        )
        returned_payload = response["Payload"].read().decode()
        if response["ResponseMetadata"]["HTTPStatusCode"] > 299:
            raise Exception(
                f"Lambda Invoke failed: {response}\n\nPayload: {returned_payload}"
            )
        if sync:
            try:
                returned_payload_dict = json.loads(returned_payload)
                if "errorMessage" in returned_payload_dict:
                    raise Exception(returned_payload_dict)
                return returned_payload_dict
            except:
                print(f"Could not load Payload as JSON: {returned_payload}")
                return returned_payload
        else:
            return response["ResponseMetadata"]["RequestId"]

    def invoke_container(
        self, container_name: str, payload: dict, sync: bool = True, timeout: int = None
    ) -> Optional[str]:
        raise NotImplementedError()
