// Fetch tasks from the API and display them
function fetchTasks() {
    fetch('http://127.0.0.1:5001/api/tasks') // Updated API endpoint
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const tasksContainer = document.getElementById('tasks');
            tasksContainer.innerHTML = ''; // Clear previous tasks

            if (data.tasks && data.tasks.length > 0) {
                data.tasks.forEach(task => {
                    const taskElement = document.createElement('div');
                    taskElement.className = 'task';
                    taskElement.innerHTML = `
                        <h3>${task.description}</h3>
                        <p><strong>tasktitle:</strong> ${task.tasktitle}</p>
                        <p><strong>Assignee:</strong> ${task.assignee}</p>
                        <p><strong>Start Date:</strong> ${task.start_date}</p>
                        <p><strong>End Date:</strong> ${task.end_date}</p>
                    `;
                    tasksContainer.appendChild(taskElement);
                });
            } else {
                tasksContainer.innerHTML = '<p>No tasks available.</p>';
            }
        })
        .catch(err => console.error('Failed to fetch tasks:', err));
}

// Add a new task to the database via API
function addTask(event) {
    event.preventDefault(); // Prevent form submission

    const tasktitle = document.getElementById('taskTitle').value;
    const taskDescription = document.getElementById('taskDescription').value;
    const taskAssignee = document.getElementById('taskAssignee').value;
    const taskStartDate = document.getElementById('taskStartDate').value;
    const taskEndDate = document.getElementById('taskEndDate').value;

    fetch('http://127.0.0.1:5001/api/tasks', { // Updated API endpoint
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            tasktitle: tasktitle,
            description: taskDescription,
            assignee: taskAssignee,
            start_date: taskStartDate,
            end_date: taskEndDate,
        }),
    })
        .then(response => {
            if (response.ok) {
                fetchTasks(); // Refresh task list
                document.getElementById('taskForm').reset(); // Reset the form
            } else {
                return response.json().then(errData => {
                    alert(`Failed to add task: ${errData.error}`);
                });
            }
        })
        .catch(err => console.error('Error adding task:', err));
}

// Fetch tasks on page load
document.addEventListener('DOMContentLoaded', fetchTasks);
