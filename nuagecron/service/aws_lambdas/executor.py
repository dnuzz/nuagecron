from typing import Any

from nuagecron.core.functions.executor import main


def lambda_handler(payload: Any, context: Any):
    schedule_id: str = payload["schedule_id"]
    execution_time: int = payload["execution_time"]
    main(schedule_id, execution_time)
