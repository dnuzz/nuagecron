from copy import deepcopy
from typing import Dict, Optional, List, Tuple
from enum import Enum
import os
from collections import Counter

from pydantic import BaseModel, constr, root_validator, validator, Field

from nuagecron.core.executors import EXECUTOR_MAP
from nuagecron.core.models.executions import ExecutionStatus
from nuagecron.core.models.utils import get_next_runtime, get_schedule_id

EXECUTION_STATUS_LIMIT = int(os.environ.get('NUAGECRON_EXECUTION_STATUS_LIMIT', 5))

class ConcurrencyAction(str, Enum):
    ready = "ready"
    block = "block"
    skip = "skip"

class Schedule(BaseModel):

    class Config:
        validate_assignment = True

    schedule_id: constr(to_lower=True, strip_whitespace=True)
    name: constr(to_lower=True, strip_whitespace=True)
    project_stack: Optional[constr(to_lower=True, strip_whitespace=True)]
    payload: dict
    cron: str
    next_run: int
    executor: str
    concurrent_runs: int = 1  # -1 is infinite, 0 is block till ready, =<1 is skipping
    overrides_applied: bool = False
    original_settings: dict = {}
    metadata: Optional[dict]
    execution_history: Dict[int, ExecutionStatus] = {}
    enabled: Optional[bool] = True

    @validator("executor")
    def executor_type_validator(cls, v):
        if v not in EXECUTOR_MAP.keys():
            raise ValueError(
                f'{v} is not a valid Executor. Valid executors are: [{",".join(EXECUTOR_MAP.keys())}]'
            )
        return v

    @root_validator(pre=True)
    def root_validation(cls, values):
        values["next_run"] = int(get_next_runtime(values["cron"]).timestamp())
        values["schedule_id"] = get_schedule_id(values["name"], values["project_stack"])
        return values

    def upsert_execution_history(self, time: int, status: ExecutionStatus) -> None:
        self.execution_history[time] = status
        sorted_keys = sorted(self.execution_history.keys(), reverse=True)[:EXECUTION_STATUS_LIMIT:]
        self.execution_history = { x: self.execution_history[x] for x in sorted_keys}

    def concurrency_limit(self) -> ConcurrencyAction:
        counts = Counter(self.execution_history.values())
        if self.concurrent_runs > 0:
            if counts[ExecutionStatus.running] >= self.concurrent_runs:
                return ConcurrencyAction.skip
            else:
                return ConcurrencyAction.ready
        elif self.concurrent_runs == 0 and counts[ExecutionStatus.running] > 0:
            return ConcurrencyAction.block
        elif self.concurrent_runs == -1:
            return ConcurrencyAction.ready
        raise ValueError('There is something wrong with the logic in the concurrency limits')