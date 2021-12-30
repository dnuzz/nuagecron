from typing import Tuple
from nuagecron.domain.executors.base_executor import BaseExecutor
from nuagecron.domain.models.executions import ExecutionStatus


class LambdaExecutor(BaseExecutor):
    class PayloadValidation(BaseExecutor.PayloadValidation):
        lambda_name: str

    """
    This should be called on creation of a schedule to ensure that any resources are available that the executor needs. (Deploy time validation)
    """

    def validate(self):
        raise NotImplementedError()

    """
    This should prepare the parameters and store them locally for a run that will happen immedaitely after. This can include expanding templates.
    """

    def prepare(self):
        raise NotImplementedError()

    """
    This should set the invoke_time and the execution_id on the execution object as well as perform the actions requested. It should return an Optional execution_id for tracking purposes and the state the execution is in
    """

    def execute(
        self,
    ) -> Tuple[
        dict, ExecutionStatus
    ]:  # This should return the execution_id and ExecutionStatus
        raise NotImplementedError()

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
