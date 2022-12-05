from time import time
from typing import Any
from logging import getLogger

from nuagecron import SERVICE_NAME
from nuagecron.core.adapters.base_database_adapter import BaseDBAdapter
from nuagecron.core.adapters.base_compute_adapter import BaseComputeAdapter
from nuagecron.core.models.schedules import ConcurrencyAction
from nuagecron.core.models.executions import Execution, ExecutionStatus
from nuagecron.core.models.utils import get_next_runtime

LOG = getLogger()


def main(compute_adapter: BaseComputeAdapter, db_adapter: BaseDBAdapter):
    start_time = time()
    timeout = 60 * 14  # about 14 minutes
    ready_schedules = db_adapter.get_schedules_to_run()
    while ready_schedules:
        for schedule in ready_schedules:
            # TODO check for concurrent_run limits using execution_history
            concurrency_action = schedule.concurrency_limit()
            if concurrency_action == ConcurrencyAction.skip:
                schedule.next_run = int(get_next_runtime(schedule.cron).timestamp())
                db_adapter.update_schedule(
                    schedule.schedule_id, {"next_run": schedule.next_run}
                )
                LOG.info(
                    f"Schedule {schedule.project_stack}/{schedule.name} is set to be skipped so it will be retried on {schedule.next_run}"
                )
            elif concurrency_action == ConcurrencyAction.block:
                LOG.info(
                    f"Schedule {schedule.project_stack}/{schedule.name} is set to be blocked so will be retried on next run of tick"
                )
            elif concurrency_action == ConcurrencyAction.ready:
                schedule_as_dict = schedule.dict()
                schedule_as_dict["execution_time"] = schedule.next_run
                schedule_as_dict["status"] = ExecutionStatus.ready
                new_execution = Execution(**schedule_as_dict)
                db_adapter.put_execution(new_execution)
                compute_adapter.invoke_function(
                    f"{SERVICE_NAME}-executor",
                    {
                        "schedule_id": schedule.schedule_id,
                        "execution_time": schedule.next_run,
                    },
                    sync=False,
                )
                LOG.info(
                    f"Schedule {schedule.project_stack}/{schedule.name} was invoked with execution time {schedule.next_run}"
                )
                schedule.upsert_execution_history(
                    schedule.next_run, ExecutionStatus.ready
                )
                schedule.next_run = int(get_next_runtime(schedule.cron).timestamp())
                db_adapter.update_schedule(
                    schedule.schedule_id, {"next_run": schedule.next_run}
                )
            if time() - start_time > timeout:
                LOG.info("Timeout limit hit. Ending run of tick")
                return
        ready_schedules = db_adapter.get_schedules_to_run()
