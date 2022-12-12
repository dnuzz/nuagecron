from flask import Flask, jsonify, make_response, request, send_from_directory
from flask_cors import CORS
from nuagecron.adapters.aws.adapters import AWSComputeAdapter, DynamoDbAdapter
from nuagecron.core.handlers.executions import ExecutionHandler
from nuagecron.core.handlers.schedules import ScheduleHandler
from nuagecron.core.functions.tick import main as tick_main


app = Flask(__name__, static_url_path="", static_folder="../frontend/build")
CORS(app)

DB_ADAPTER = DynamoDbAdapter()
COMPUTE_ADAPTER = AWSComputeAdapter()

SCHEDULE_HANDLER = ScheduleHandler(DB_ADAPTER, COMPUTE_ADAPTER)
EXECUTION_HANDLER = ExecutionHandler(DB_ADAPTER, COMPUTE_ADAPTER)


@app.route("/schedules")
def get_schedules():
    schedules, _ = SCHEDULE_HANDLER.get_all_schedules(request.args.get("start_key"))

    return jsonify([s.dict() for s in schedules])


@app.route("/schedule/<string:name>/<string:project_stack>")
def get_schedule(name: str, project_stack: str = None):
    schedule = SCHEDULE_HANDLER.get_schedule(name, project_stack)

    if not schedule:
        return (
            jsonify(
                {
                    "error": "No schedule found",
                    "name": name,
                    "project_stack": project_stack,
                }
            ),
            404,
        )
    return jsonify(schedule.dict())


@app.route("/schedules/create", methods=["PUT"])
def create_schedule():
    schedule = SCHEDULE_HANDLER.create_schedule(request.json)

    return jsonify(schedule.dict())


@app.route("/schedules/<string:project_stack>", methods=["GET"])
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


@app.route("/executions/<string:schedule_id>", methods=["get"])
def get_executions(schedule_id: str):
    executions = DB_ADAPTER.get_executions(schedule_id)
    return jsonify(executions)


@app.route("/executions/<string:schedule_id>/<int:execution_time>", methods=["get"])
def get_execution(schedule_id: str, execution_time: int):
    execution = DB_ADAPTER.get_execution(schedule_id, execution_time)
    return jsonify(execution)


@app.route("/tick", methods=["post"])
def run_tick():
    tick_main(COMPUTE_ADAPTER, DB_ADAPTER)
    return make_response({}, 202)


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error="Not found!"), 404)


@app.route("/", defaults={"path": ""})
def serve(path):
    return send_from_directory(app.static_folder, "index.html")
