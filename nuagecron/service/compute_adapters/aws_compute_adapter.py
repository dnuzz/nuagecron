from typing import Optional
from nuagecron.service.compute_adapters.base_compute_adapter import BaseComputeAdapter
import boto3
import json

LAMBDA_CLIENT = boto3.client("lambda")
FARGATE_CLIENT = boto3.client("fargate")


class AWSComputeAdapter(BaseComputeAdapter):
    def __init__(self) -> None:
        super().__init__()

    def invoke_function(
        self, function_name: str, payload: dict, sync: bool = True, timeout: int = None
    ) -> dict:
        payload_str = str.encode(json.dumps(payload, default=str))
        if sync:
            invoke_type = "RequestResponse"
        else:
            invoke_type = "Event"
        response = LAMBDA_CLIENT.invoke(
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
            except:
                print(f"Could not load Payload as JSON: {returned_payload}")
                return returned_payload
            if "errorMessage" in returned_payload_dict:
                raise Exception(returned_payload_dict)
        else:
            return response["ResponseMetadata"]["RequestId"]

    def invoke_container(
        self, container_name: str, payload: dict, sync: bool = True, timeout: int = None
    ) -> Optional[str]:
        raise NotImplementedError()
