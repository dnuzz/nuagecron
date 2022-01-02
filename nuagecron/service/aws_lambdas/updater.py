from typing import Any

from nuagecron.domain.functions.updater import main


def _get_execution_id(payload: dict) -> str:
    raise NotImplementedError()


def lambda_handler(payload: dict, context: dict):
    execution_id = _get_execution_id(payload)
    main(execution_id, payload)
