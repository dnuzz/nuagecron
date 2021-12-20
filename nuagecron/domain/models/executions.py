from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum

class ExecutionStatus(str, Enum):
    ready = 'ready'
    skipped = 'skipped'
    running = 'running'
    failed = 'failed'
    timed_out = 'timed_out'

class Execution(BaseModel):

    class Meta:
        extra = 'allow'

    schedule_id: str
    execution_time: int
    payload: dict
    invoke_time: Optional[datetime]
    update_time: Optional[datetime]
    execution_id: Optional[str]
    status: ExecutionStatus