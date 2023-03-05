from typing import Union
from flask import (
    Flask,
    jsonify,
    make_response,
    request,
    send_from_directory,
    Blueprint,
    url_for,
)
import os
from flask_cors import CORS
import requests
from yaml import safe_load
from nuagecron.adapters.aws.adapters import AWSComputeAdapter, DynamoDbAdapter
from nuagecron.core.handlers.executions import ExecutionHandler
from nuagecron.core.handlers.schedules import ScheduleHandler
from nuagecron.core.functions.tick import main as tick_main
from nuagecron.core.functions.executor import main as executor_main
from nuagecron import SERVICE_NAME
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__, static_folder="../frontend/build")
app.secret_key = "abc"
CORS(app)

DB_ADAPTER = DynamoDbAdapter()
COMPUTE_ADAPTER = AWSComputeAdapter()

SCHEDULE_HANDLER = ScheduleHandler(DB_ADAPTER, COMPUTE_ADAPTER)
EXECUTION_HANDLER = ExecutionHandler(DB_ADAPTER, COMPUTE_ADAPTER)

api = Blueprint("api", __name__)


@api.route("/schedules")
def get_schedules():
    schedules, _ = SCHEDULE_HANDLER.get_all_schedules(request.args.get("start_key"))

    return jsonify([s.dict() for s in schedules])


@api.route("/schedule/<string:schedule_id>")
def get_schedule(
    schedule_id: str,
):
    schedule = SCHEDULE_HANDLER.get_schedule_by_id(schedule_id)

    if not schedule:
        return (
            jsonify({"error": "No schedule found", "schedule_id": schedule_id}),
            404,
        )
    return jsonify(schedule.dict())


@api.route("/schedule/<string:schedule_id>/invoke", methods=["POST"])
def invoke_schedule(
    schedule_id: str,
):
    schedule = SCHEDULE_HANDLER.get_schedule_by_id(schedule_id)

    if not schedule:
        return (
            jsonify({"error": "No schedule found", "schedule_id": schedule_id}),
            404,
        )
    execution = EXECUTION_HANDLER.create_execution(
        schedule.name, schedule.project_stack
    )
    if request.args.get("sync"):
        executor_main(DB_ADAPTER, schedule.schedule_id, execution.execution_time)
    else:
        COMPUTE_ADAPTER.invoke_function(
            f"{SERVICE_NAME}-executor",
            {
                "schedule_id": schedule.schedule_id,
                "execution_time": execution.execution_time,
            },
            sync=False,
        )
    return jsonify(execution.dict())

def check_content_for_request(request) -> Union[dict, tuple]:
    if request.content_type.lower() == 'application/json':
        payload = request.json()
    elif request.content_type.lower() == 'text/plain':
        payload = safe_load(request.stream)
    else:
        return (jsonify({"error": "Content-type must be application/json (for json document) or text/plain (If using a yaml document)"}), 406)
    return payload

@api.route("/schedules/create", methods=["PUT"])
def create_schedule():
    payload = check_content_for_request(request)
    if isinstance(payload, tuple):
        return payload

    schedule = SCHEDULE_HANDLER.create_schedule(payload)

    return jsonify(schedule.dict())

@api.route("/schedule_set/create", methods=["PUT"])
def create_schedule_set():
    payload = check_content_for_request(request)
    if isinstance(payload, tuple):
        return payload
    schedule = SCHEDULE_HANDLER.upsert_schedule_set(payload)
    return jsonify(schedule.dict())


@api.route("/schedule_set/<string:project_stack>", methods=["GET"])
def get_stack_schedules(project_stack: str = None):
    if project_stack:
        retval = DB_ADAPTER.get_schedule_set(project_stack)
        if not retval:
            return (
                jsonify(
                    {"error": "No project stack found", "project_stack": project_stack}
                ),
                404,
            )
    else:
        start_key = request.json.get("start_key")
        return jsonify(DB_ADAPTER.get_schedules(start_key))


@api.route("/executions/<string:schedule_id>", methods=["GET"])
def get_executions(schedule_id: str):
    executions = DB_ADAPTER.get_executions(schedule_id)
    return jsonify([e.dict() for e in executions[0]])


@api.route("/executions/<string:schedule_id>/<int:execution_time>", methods=["get"])
def get_execution(schedule_id: str, execution_time: int):
    execution = DB_ADAPTER.get_execution(schedule_id, execution_time)
    return jsonify(execution)


@api.route("/tick", methods=["post"])
def run_tick():
    tick_main(COMPUTE_ADAPTER, DB_ADAPTER)
    return make_response({}, 202)


@api.route("/token", methods=["POST"])
def get_auth_token():
    parameters = {
        **request.form,
        **{
            "client_id": os.getenv("OAUTH_CLIENT_ID"),
            "client_secret": os.getenv("OAUTH_CLIENT_SECRET"),
        },
    }
    response = requests.post(
        os.getenv("OAUTH_DOMAIN") + os.getenv("OAUTH_TOKEN_ENDPOINT"),
        params=parameters,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    response.raise_for_status()
    # user_info = requests.get(os.getenv("OAUTH_DOMAIN") + "/oauth2/userInfo", headers={"Authorization": f"Bearer {response.json()['access_token']}", "Content-Type": "application/json"})
    # ret_val = {**user_info.json(), **response.json()}
    return response.json()


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    if path != "" and os.path.exists(app.static_folder + "/" + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")


app.register_blueprint(api, url_prefix="/api")
