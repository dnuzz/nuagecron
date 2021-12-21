from nuagecron.domain.executors.base_executor import BaseExecutor


class LambdaExecutor(BaseExecutor):
    class PayloadValidation(BaseExecutor.PayloadValidation):
        lambda_name: str

    def validate(self):
        raise NotImplementedError()

    """
    This should validate the params to the best of it's ability using the payload
    """

    def prepare(self):
        raise NotImplementedError()

    """
    This should set the invoke_time and the execution_id on the execution object
    """

    def execute(self):  # This should set the invoke time and the execution_id
        raise NotImplementedError()

    """
    When an update is passed to this it should update the execution and the update_time attributes
    """

    def process_update(self, update: dict):
        raise NotImplementedError()

    """
    This should attempt to kill the running execution and return whether that was successful or not
    """

    def try_kill(self) -> bool:
        raise NotImplementedError()
