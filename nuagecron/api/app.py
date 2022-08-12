import os

import boto3
from flask import Flask, jsonify, make_response, request, send_from_directory

app = Flask(__name__, static_url_path='', static_folder='frontend')


dynamodb_client = boto3.client("dynamodb")

if os.environ.get("IS_OFFLINE"):
    dynamodb_client = boto3.client(
        "dynamodb", region_name="localhost", endpoint_url="http://localhost:8000"
    )


SCHEDULES_TABLE = os.environ["SCHEDULES_TABLE"]


@app.route("/users/<string:user_id>")
def get_user(user_id):
    result = dynamodb_client.get_item(
        TableName=SCHEDULES_TABLE, Key={"userId": {"S": user_id}}
    )
    item = result.get("Item")
    if not item:
        return jsonify({"error": 'Could not find user with provided "userId"'}), 404

    return jsonify(
        {"userId": item.get("userId").get("S"), "name": item.get("name").get("S")}
    )


@app.route("/users", methods=["POST"])
def create_user():
    user_id = request.json.get("userId")
    name = request.json.get("name")
    if not user_id or not name:
        return jsonify({"error": 'Please provide both "userId" and "name"'}), 400

    dynamodb_client.put_item(
        TableName=SCHEDULES_TABLE,
        Item={"schedule_id": {"S": user_id}, "name": {"S": name}},
    )

    return jsonify({"userId": user_id, "name": name})


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error="Not found!"), 404)

@app.route("/", defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')