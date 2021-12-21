
from typing import Any
from nuagecron import SERVICE_NAME
from nuagecron.domain.models.executions import Execution
from nuagecron.service.lambdas.utils import get_compute_adapter, get_db_adapter
from nuagecron.domain.utils.utils import get_next_runtime
from time import time

def lambda_handler(payload: Any, Context: Any):
    start_time = time()
    timeout = 60*14 # about 14 minutes
    db_adapter = get_db_adapter()
    compute_adapter = get_compute_adapter()
    ready_schedules = db_adapter.get_schedules_to_run()
    for schedule in ready_schedules:
        schedule_as_dict = schedule.dict()
        schedule_as_dict['execution_time'] = schedule.next_run
        new_execution = Execution(**schedule_as_dict)
        db_adapter.put_execution(new_execution)
        compute_adapter.invoke_function(f'{SERVICE_NAME}-executor', {'schedule_id': schedule.schedule_id, 'execution_time': schedule.next_run}, sync=False)
        schedule.next_run = int(get_next_runtime(schedule.cron).timestamp())
        if time() - start_time > timeout:
            return
