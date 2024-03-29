from typing import Optional, Tuple

from nuagecron.core.executors import BaseExecutor
from nuagecron.core.executors import register_executor
from nuagecron.core.models.executions import ExecutionStatus
from nuagecron.core.models.executions import Execution
import boto3
import json

LAMBDA_CLIENT = boto3.client("lambda")


@register_executor
class LambdaExecutor(BaseExecutor):
    class PayloadValidation(BaseExecutor.PayloadValidation):
        lambda_name: str

    def __init__(self, execution: Execution):
        super().__init__(execution)

    """
    This should be called on creation of a schedule to ensure that any resources are available that the executor needs. (Deploy time validation)
    """

    def validate(self):
        resp = LAMBDA_CLIENT.invoke(
            FunctionName=self.payload["lambda_name"], InvocationType="DryRun"
        )
        if resp["StatusCode"] != 204:
            raise ValueError("Could not validate function")

    """
    This should prepare the parameters and store them locally for a run that will happen immedaitely after. This can include expanding templates.
    """

    def prepare(self):
        return

    """
    This should set the invoke_time and the execution_id on the execution object as well as perform the actions requested. It should return an Optional execution_id for tracking purposes and the state the execution is in
    """

    def execute(
        self,
    ) -> Tuple[
        Optional[str], ExecutionStatus
    ]:  # This should return the execution_id and ExecutionStatus
        resp = LAMBDA_CLIENT.invoke(
            FunctionName=self.payload["lambda_name"],
            InvocationType="Event",
            Payload=json.dumps(
                self.payload.get("lambda_payload", {}), default=str
            ).encode(),
        )
        if resp["StatusCode"] != 202 or resp.get("FunctionError"):
            return None, ExecutionStatus.failed
        return None, ExecutionStatus.succeeded

    """
    When an update is passed to this it should update the execution and the update_time attributes
    """

    def process_update(self, update: dict) -> dict:
        raise NotImplementedError()

    """
    This should attempt to kill the running execution and return whether that was successful or not
    """

    def try_kill(self) -> bool:
        raise NotImplementedError()
