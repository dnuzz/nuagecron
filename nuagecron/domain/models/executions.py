from pydantic import BaseModel
from nuagecron import SERVICE_NAME

class Execution(BaseModel):

    class Meta:
        DYNAMODB_TABLE = f'{SERVICE_NAME}-executions'

    schedule_id: str
    execution_time: float
    payload: dict