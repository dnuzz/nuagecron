from pydantic import BaseModel
from nuagecron import SERVICE_NAME

class Schedule(BaseModel):
    
    class Meta:
        DYNAMODB_TABLE = f'{SERVICE_NAME}-schedules'

    schedule_id: str
    payload: dict