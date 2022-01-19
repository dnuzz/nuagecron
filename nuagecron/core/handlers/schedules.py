from typing import Dict, List, Optional
from nuagecron.core.adapters.base_compute_adapter import BaseComputeAdapter
from nuagecron.core.adapters.base_database_adapter import BaseDBAdapter
from nuagecron.core.models.utils import get_schedule_id

from nuagecron.core.models.schedules import Schedule
from nuagecron.core.models.schedule_set import ScheduleSet


class ScheduleHandler:
    def __init__(
        self, db_adapter: BaseDBAdapter, compute_adapter: BaseComputeAdapter
    ) -> None:
        self.db_adapter = db_adapter
        self.compute_adapter = compute_adapter

    def create_schedule(self, payload: dict) -> Schedule:
        schedule = Schedule(**payload)
        self.db_adapter.put_schedule(schedule)
        return schedule

    def upsert_schedule_set(self, payload: dict) -> Dict[str, List[Schedule]]:
        new_schedule_set = ScheduleSet(**payload)
        schedule_list = [x for x in new_schedule_set.schedules]
        self.db_adapter.put_schedule_set(schedule_list)

    def get_schedule(
        self, name: str, project_stack: Optional[str] = None
    ) -> Optional[Schedule]:
        return self.db_adapter.get_schedule(get_schedule_id(name, project_stack))

    def get_schedule_set(self, project_stack: str) -> List[Schedule]:
        return self.db_adapter.get_schedule_set(project_stack)

    def update_schedule(
        self, name: str, project_stack: Optional[str] = None, payload: dict = {}
    ) -> Schedule:
        return self.db_adapter.update_schedule(get_schedule_id(name, project_stack))

    def apply_overrides_to_schedule(
        self, name: str, project_stack: Optional[str], payload: dict
    ) -> Schedule:
        schedule_id = get_schedule_id(name, project_stack)
        schedule = self.db_adapter.get_schedule(schedule_id)
        schedule_dict = schedule.dict()
        schedule_dict.update(payload)
        Schedule(**schedule_dict) # TODO add better validation that the schedule updates were appropriate
        payload['overrides_applied'] = True
        self.db_adapter.update_schedule(schedule_id, payload)
        return self.db_adapter.get_schedule(schedule_id)

    def reset_schedule(self, name: str, project_stack: Optional[str]) -> bool:
        schedule_id = get_schedule_id(name, project_stack)
        schedule = self.db_adapter.get_schedule(schedule_id)
        self.db_adapter.update_schedule(schedule_id, schedule.original_settings)
        return True

