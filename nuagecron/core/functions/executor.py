from nuagecron.core.adapters.base_database_adapter import BaseDBAdapter
from nuagecron.core.executors import EXECUTOR_MAP
from nuagecron.core.models.executions import ExecutionStatus


def main(db_adapter: BaseDBAdapter, schedule_id: str, execution_time: int):
    execution = db_adapter.get_execution(schedule_id, execution_time)
    schedule = db_adapter.get_schedule(schedule_id)
    status: ExecutionStatus = ExecutionStatus.ready
    try:
        executor_class = EXECUTOR_MAP[execution.executor]
        executor = executor_class(execution)
        executor.prepare()
    except:
        status = ExecutionStatus.internal_error
    execution_id, status = executor.execute()
    schedule.upsert_execution_history(schedule.next_run, status)
    db_adapter.update_schedule(
        schedule_id, {"execution_history": schedule.execution_history}
    )
    execution.execution_id = execution_id
    execution.status = status
    db_adapter.update_execution(
        schedule_id, execution_time, {"execution_id": execution_id, "status": status}
    )
    # TODO update the exection_history in the schedule object
