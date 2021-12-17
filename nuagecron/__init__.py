from os import path
import json
SERVICE_NAME = json.load(open(path.join(path.dirname(__file__),'servicename.json')))['servicename']