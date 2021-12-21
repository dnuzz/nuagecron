from crontab import CronTab
import crontab
from datetime import datetime


def get_next_runtime(cron: str) -> datetime:
    if cron == "MANUAL":
        nextrun = datetime.max
    else:
        cron_tab = CronTab(cron)
        return cron_tab.next(default_utc=True, return_datetime=True)


def get_schedule_id(name: str, project_stack: str):
    return f"{name}_{project_stack}".replace(" ", "_").replace("-", "_").lower()
