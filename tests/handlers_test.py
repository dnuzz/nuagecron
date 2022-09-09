from nuagecron.core.handlers.executions import ExecutionHandler
from nuagecron.core.handlers.schedules import ScheduleHandler
from nuagecron.core.models.schedules import Schedule
from .adapters import MockComputeAdapter, MockDatabaseAdapter

DB_ADAPTER = MockDatabaseAdapter()
COMPUTE_ADAPTER = MockComputeAdapter(DB_ADAPTER)

TEST_SCHEDULE = {
    "name": "test",
    "project_stack": None,
    "payload": {"a": "a"},
    "cron": "0 5 * * *",
    "executor": "MockExecutor",
}


def test_schedule_hanlder():
    handler = ScheduleHandler(DB_ADAPTER, COMPUTE_ADAPTER)
    schedule = handler.create_schedule(TEST_SCHEDULE)
    assert schedule
    schedule = handler.get_schedule("test", None)
    assert schedule
    handler.apply_overrides_to_schedule("test", None, {"payload": {"a": "b"}})
    schedule = handler.get_schedule("test", None)
    assert schedule.payload["a"] == "b"
    handler.reset_schedule("test", None)


def test_execution_handler():
    handler = ExecutionHandler(DB_ADAPTER, COMPUTE_ADAPTER)
