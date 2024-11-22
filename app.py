from flask import Flask, request, render_template, redirect
import requests

app = Flask(__name__)
API_URL = "http://127.0.0.1:5001/api/tasks"  # API endpoint

@app.route('/')
def index():
    """
    Fetch tasks from the API and display them.
    """
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            tasks = data.get('tasks', [])
        else:
            tasks = []
            print(f"Error fetching tasks: {response.status_code}")
    except requests.exceptions.RequestException as e:
        tasks = []
        print(f"API request failed: {e}")
    
    return render_template('index.html', tasks=tasks)

@app.route("/add_task", methods=["POST"])
def add_task():
    """
    Add a new task via the API.
    """
    task_data = {
        "tasktitle": request.form["tasktitle"],
        "description": request.form["description"],
        "start_date": request.form["start_date"],
        "end_date": request.form["end_date"],
        "assignee": request.form["assignee"]
    }

    try:
        response = requests.post(API_URL, json=task_data)
        if response.status_code == 201:
            return redirect('/')
        else:
            return "Failed to add task", 400
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return "API connection error", 500

@app.route("/delete_task/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    """
    (Optional) Implement task deletion if needed.
    """
    # To be implemented on the API side if required
    return "Delete functionality not implemented yet."

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
