import json
from os import environ, path

_SERVICENAME_JSON = json.load(open("servicename.json")) if path.exists("servicename.json") else {}

SERVICE_NAME = environ.get(
    "NUAGECRON_SERVICE_NAME",
    _SERVICENAME_JSON.get("servicename", 'nuagecron'),
)
CLOUD_PROVIDER = environ.get(
    "NUAGECRON_CLOUD_PROVDER",
    _SERVICENAME_JSON.get("cloud_provider", 'AWS'),
)

__all__ = ['SERVICE_NAME', 'CLOUD_PROVIDER']