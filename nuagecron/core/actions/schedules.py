from typing import Dict, List, Optional

from nuagecron.core.models.schedules import Schedule


def create_schedule(payload: dict) -> Schedule:
    pass


def upsert_schedule_set(payload: dict) -> Dict[str, List[Schedule]]:
    pass


def get_schedule(name: str, project_stack: Optional[str]) -> Schedule:
    pass


def get_schedule_set(name: str, project_stack: Optional[str]) -> List[Schedule]:
    pass


def update_schedule(name: str, project_stack: Optional[str], payload: dict) -> Schedule:
    pass


def apply_overrides_to_schedule(
    name: str, project_stack: Optional[str], payload: dict
) -> Schedule:
    pass


def reset_schedule(name: str, project_stack: Optional[str]) -> bool:
    pass
