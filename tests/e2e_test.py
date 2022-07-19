from core.models.executions import Execution
from .adapters import MockComputeAdapter, MockDatabaseAdapter, MockExecutor
from nuagecron.core.models.schedules import Schedule
from nuagecron.core.functions.executor import main as executor_main
from nuagecron.core.functions.updater import main as updater_main
from nuagecron.core.functions.tick import main as tick_main
from datetime import datetime

DB_ADAPTER = MockDatabaseAdapter()
COMPUTE_ADAPTER = MockComputeAdapter(DB_ADAPTER)

TEST_SCHEDULE = Schedule(
    name="test",
    project_stack=None,
    payload={"lambda_name": "a"},
    cron="1 * * * *",
    executor="LambdaExecutor",
)
EXECUTION_DICT = TEST_SCHEDULE.dict()
EXECUTION_DICT.update(
    {"execution_time": 1, "status": "running", "execution_id": "test_id"}
)
TEST_EXECUTION = Execution(**EXECUTION_DICT)


def test_tick():
    DB_ADAPTER.put_schedule(TEST_SCHEDULE)
    tick_main(COMPUTE_ADAPTER, DB_ADAPTER)


def test_executor():
    DB_ADAPTER.put_schedule(TEST_SCHEDULE)
    DB_ADAPTER.put_execution(TEST_EXECUTION)
    executor_main(DB_ADAPTER, TEST_SCHEDULE.schedule_id, 1)


def test_updater():
    DB_ADAPTER.put_execution(TEST_EXECUTION)
    updater_main(DB_ADAPTER, "test_id", {"status": "succeeded"})
