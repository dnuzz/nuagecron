from typing import Dict, Optional

from pydantic import BaseModel, root_validator, validator

from nuagecron.core.models.schedules import Schedule


class ScheduleSet(BaseModel):
    defaults: dict = {}
    project_stack: str
    schedules: Dict[str, Schedule] = {}

    @root_validator(pre=True)
    def root_validate_schedule_set(cls, values):
        if schedules := values.get("schedules"):
            values['schedules'] = dict()
            if not isinstance(schedules, list):
                raise ValueError('Please specify schedules as a list when creating a schedule set')
            for schedule in schedules:
                updated_schedule = values.get("defaults", {}).update(schedules)
                updated_schedule["project_stack"] = values["project_stack"]
                s = Schedule(**updated_schedule)
                values['schedules'][s.schedule_id] = s
        return values
