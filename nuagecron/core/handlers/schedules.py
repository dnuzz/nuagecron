from copy import deepcopy
from typing import Dict, List, Optional
from nuagecron.core.adapters.base_compute_adapter import BaseComputeAdapter
from nuagecron.core.adapters.base_database_adapter import BaseDBAdapter
from nuagecron.core.models.utils import get_schedule_id

from nuagecron.core.models.schedules import Schedule
from nuagecron.core.models.schedule_set import ScheduleSet

# TODO This may not even be needed or should maybe live in the api layer
class ScheduleHandler:
    def __init__(
        self, db_adapter: BaseDBAdapter, compute_adapter: BaseComputeAdapter
    ) -> None:
        self.db_adapter = db_adapter
        self.compute_adapter = compute_adapter

    def create_schedule(self, payload: dict) -> Schedule:
        if "original_settings" in payload:
            del payload["original_settings"]
        schedule = Schedule(**payload)
        schedule.original_settings = payload
        self.db_adapter.put_schedule(schedule)
        return schedule

    def upsert_schedule_set(self, payload: dict) -> Dict[str, List[Schedule]]:
        new_schedule_set = ScheduleSet(**payload)
        new_schedules = new_schedule_set.schedules
        old_schedules: Dict[str, Schedule] = {
            x.schedule_id: x
            for x in self.db_adapter.get_schedule_set(new_schedule_set.project_stack)
        }
        keys_to_delete = old_schedules.keys() - new_schedules.keys()
        keys_to_add = new_schedules.keys() - old_schedules.keys()
        keys_to_update = set(new_schedules.keys()).intersection(old_schedules.keys())
        put_list: List[Schedule] = []
        update_list: List[Schedule] = []
        delete_list: List[Schedule] = []
        for key in keys_to_add:
            put_list.append(new_schedules[key])
        for key in keys_to_update:
            updated_dict = (
                old_schedules[key]
                .dict(exclude_unset=True)
                .update(new_schedules[key].dict(exclude_unset=True))
            )
            updated = Schedule(**updated_dict)
            update_list.append(updated)
        for key in keys_to_delete:
            delete_list.append(old_schedules[key])

        for x in put_list:
            self.db_adapter.put_schedule(x)
        for x in update_list:
            self.db_adapter.update_schedule(
                x.schedule_id, x.dict(exclude_unset=True, exclude_defaults=True)
            )
        for x in delete_list:
            self.db_adapter.delete_schedule(x.schedule_id)
        return {"added": put_list, "deleted": delete_list, "updated": update_list}

    def get_schedule(
        self, name: str, project_stack: Optional[str] = None
    ) -> Optional[Schedule]:
        return self.db_adapter.get_schedule(get_schedule_id(name, project_stack))

    def get_schedule_by_id(self, schedule_id: str) -> Optional[Schedule]:
        return self.db_adapter.get_schedule(schedule_id)

    def get_schedule_set(self, project_stack: str) -> List[Schedule]:
        return self.db_adapter.get_schedule_set(project_stack)

    def update_schedule(
        self, name: str, project_stack: Optional[str] = None, payload: dict = {}
    ) -> Schedule:
        schedule_id = get_schedule_id(name, project_stack)
        current_schedule = self.db_adapter.get_schedule(schedule_id)
        schedule_dict = current_schedule.dict()
        schedule_dict.update(payload)
        payload["original_settings"] = schedule_dict["original_settings"]
        payload["original_settings"].update(payload)
        Schedule(
            **schedule_dict
        )  # This tests to see if the changes to the schedule pass validation
        return self.db_adapter.update_schedule(
            get_schedule_id(name, project_stack), payload
        )

    def apply_overrides_to_schedule(
        self, name: str, project_stack: Optional[str], payload: dict
    ) -> Schedule:
        if "original_settings" in payload:
            del payload["original_settings"]
        payload["overrides_applied"] = True
        schedule_id = get_schedule_id(name, project_stack)
        current_schedule = self.db_adapter.get_schedule(schedule_id)
        schedule_dict = current_schedule.dict()
        schedule_dict.update(payload)
        Schedule(**schedule_dict)
        self.db_adapter.update_schedule(schedule_id, payload)
        return self.db_adapter.get_schedule(schedule_id)

    def reset_schedule(self, name: str, project_stack: Optional[str]) -> bool:
        schedule_id = get_schedule_id(name, project_stack)
        schedule = self.db_adapter.get_schedule(schedule_id)
        payload = deepcopy(schedule.original_settings)
        payload["overrides_applied"] = False
        self.db_adapter.update_schedule(schedule_id, payload)
        return True
