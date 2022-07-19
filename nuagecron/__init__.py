import json
from os import environ, path

SERVICE_NAME = environ.get(
    "NUAGECRON_SERVICE_NAME",
    json.load(open("servicename.json"))["servicename"],
)
CLOUD_PROVIDER = environ.get(
    "NUAGECRON_CLOUD_PROVDER",
    json.load(open("servicename.json"))["cloud_provider"],
)
