from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# MongoDB connection details
username = "admin"
password = "admin"
host = "mongodb"  # Use service name defined in docker-compose.yml
port = 27017
database_name = "MyAppDB"
auth_database = "admin"

# Create the connection URI
mongo_uri = f"mongodb://{username}:{password}@{host}:{port}/{database_name}?authSource={auth_database}"

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[database_name]
tasks_collection = db["tasks"]  # Initialize the tasks collection

@app.route('/api/tasks', methods=['POST'])
def add_task():
    """
    Add a task to the database.
    """
    try:
        # Parse incoming data
        task_data = request.json
        tasktitle = task_data.get("tasktitle")
        description = task_data.get("description")
        start_date = task_data.get("start_date")
        end_date = task_data.get("end_date")
        assignee = task_data.get("assignee")

        # Validate required fields
        if not all([tasktitle, description, start_date, end_date, assignee]):
            return jsonify({"error": "All fields are required"}), 400

        # Insert task into MongoDB
        task = {
            "tasktitle": tasktitle,
            "description": description,
            "start_date": start_date,
            "end_date": end_date,
            "assignee": assignee
        }
        result = tasks_collection.insert_one(task)

        return jsonify({"message": "Task added successfully", "task_id": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """
    Retrieve all tasks from the database.
    """
    try:
        tasks = list(tasks_collection.find({}, {"_id": 0}))  # Exclude MongoDB _id field
        return jsonify({"tasks": tasks}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)  # API runs on port 5001
