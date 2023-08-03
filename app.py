from flask import Flask, jsonify, request, make_response
from flask_pymongo import PyMongo
from pymongo import MongoClient
import urllib.parse
from bson.objectid import ObjectId
from bson.json_util import dumps
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

username = urllib.parse.quote_plus("xavieralamar")
password = urllib.parse.quote_plus("Soccer13091003")
app.config["MONGO_URI"] = "mongodb+srv://%s:%s@cluster0.gumkccs.mongodb.net/todo" % (
    username,
    password,
)

mongo = PyMongo(app)


@app.route("/")
def hello():
    return "Hello, Flask with PyMongo!"


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    try:
        tasks = list(mongo.db.todo.find())
        return make_response(dumps(tasks), 200)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/tasks", methods=["POST"])
def add_task():
    try:
        task = request.json.get("task")
        task_id = mongo.db.todo.insert_one({"task": task}).inserted_id
        return jsonify({"message": "Task added successfully", "id": str(task_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):
    try:
        task = request.json.get("task")
        mongo.db.todo.update_one({"_id": ObjectId(task_id)}, {"$set": {"task": task}})
        return jsonify({"message": "Task updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    try:
        mongo.db.todo.delete_one({"_id": ObjectId(task_id)})
        return jsonify({"message": "Task deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
