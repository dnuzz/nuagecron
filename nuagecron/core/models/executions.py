from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, constr


class ExecutionStatus(str, Enum):
    ready = "ready"
    skipped = "skipped"
    running = "running"
    failed = "failed"
    timed_out = "timed_out"
    killed = "killed"
    internal_error = "internal_error"
    succeeded = "succeeded"


class Execution(BaseModel):
    class Meta:
        extra = "allow"

    schedule_id: constr(to_lower=True, strip_whitespace=True)
    execution_time: int
    payload: dict
    executor: str
    invoke_time: Optional[datetime]
    update_time: Optional[datetime]
    execution_id: Optional[str]
    status: ExecutionStatus
    log_link: Optional[str]
