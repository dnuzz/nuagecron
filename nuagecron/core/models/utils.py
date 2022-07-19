from datetime import datetime
from typing import Optional

from crontab import CronTab


def get_next_runtime(cron: str) -> datetime:
    if cron == "MANUAL":
        return datetime.max
    else:
        cron_tab = CronTab(cron)
        return cron_tab.next(default_utc=True, return_datetime=True)


def get_schedule_id(name: str, project_stack: Optional[str]):
    suffix = "_" + project_stack if project_stack else ""
    return f"{name}{suffix}".replace(" ", "_").replace("-", "_").lower()
