from copy import deepcopy
from typing import Dict, Optional

from pydantic import BaseModel, constr, root_validator, validator, Field

from nuagecron.core.executors import EXECUTOR_MAP
from nuagecron.core.models.executions import ExecutionStatus
from nuagecron.core.models.utils import get_next_runtime, get_schedule_id


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
    original_settings: dict = Field(
        {},
        allow_mutation=False,
    )
    metadata: Optional[dict]
    execution_history: Optional[Dict[int, ExecutionStatus]]
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
        values["original_settings"] = deepcopy(values)
        values["next_run"] = int(get_next_runtime(values["cron"]).timestamp())
        values["schedule_id"] = get_schedule_id(values["name"], values["project_stack"])
        return values

