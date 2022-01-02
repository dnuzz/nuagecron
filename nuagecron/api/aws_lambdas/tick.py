from time import time
from typing import Any

from nuagecron.core.functions.tick import main


def lambda_handler(payload: Any, Context: Any):
    main()
