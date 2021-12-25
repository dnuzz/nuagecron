from typing import Optional, Dict
from pydantic import BaseModel, validator, root_validator
from nuagecron.domain.models.schedules import Schedule


class ScheduleSet(BaseModel):
    defaults: dict = {}
    project_stack: str
    schedules: Optional[Dict[str, Schedule]]

    @root_validator(pre=True)
    def root_validate_schedule_set(cls, values):
        if values.get("schedules"):
            for k, v in values["schedules"].items():
                updated_schedule = values.get("defaults", {}).update(v)
                updated_schedule["project_stack"] = values["project_stack"]
                values[k] = v
        return values
