from os import path, environ
import json
SERVICE_NAME = environ.get("NUAGECRON_SERVICE_NAME" ,json.load(open(path.join(path.dirname(__file__),'servicename.json')))['servicename'])