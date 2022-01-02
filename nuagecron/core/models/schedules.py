from typing import Dict, Literal, Optional

from pydantic import BaseModel, constr, root_validator, validator

from nuagecron.core.executors.base_executor import BaseExecutor
from nuagecron.core.models.executions import ExecutionStatus
from nuagecron.core.models.utils import get_next_runtime, get_schedule_id

VALID_EXECUTORS = [cls.__name__ for cls in BaseExecutor.__subclasses__()]


class Schedule(BaseModel):

    schedule_id: constr(to_lower=True, strip_whitespace=True)
    name: constr(to_lower=True, strip_whitespace=True)
    project_stack: constr(to_lower=True, strip_whitespace=True)
    payload: dict
    cron: str
    next_run: int
    executor: str
    concurrent_runs: int = 1  # -1 is infinite, 0 is block till ready, =<1 is skipping
    overrides_applied: bool = False
    metadata: Optional[dict]
    execution_history: Optional[Dict[int, ExecutionStatus]]
    enabled: Optional[bool] = True

    @validator("executor")
    def executor_name_validator(cls, v):
        if v not in VALID_EXECUTORS:
            raise ValueError(
                f'{v} is not a valid Executor. Valid executors are: [{",".join(VALID_EXECUTORS)}]'
            )
        return v

    @root_validator(pre=True)
    def root_validation(cls, values):
        values["next_run"] = int(get_next_runtime(values["cron"]).timestamp())
        values["schedule_id"] = get_schedule_id(values["name"], values["project_stack"])
        return values
