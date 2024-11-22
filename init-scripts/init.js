// Initialize MongoDB settings and user

// Create database
db = db.getSiblingDB('MyAppDB');

// Create admin user with readWrite privileges
db.createUser({
    user: "admin",
    pwd: "admin",
    roles: [
        { role: "readWrite", db: "taskappdb" },
        { role: "dbAdmin", db: "taskappdb" }
    ]
});

// Optionally, you can add additional collections and indexes

// Example: Creating a sample collection with an index
db.createCollection('tasks');
db.tasks.createIndex({ "task_id": 1 }, { unique: true });

// Adding some initial data (optional)
db.tasks.insertMany([
    { task_id: 1, name: "Sample Task 1", description: "This is a sample task", status: "in-progress" },
    { task_id: 2, name: "Sample Task 2", description: "Another sample task", status: "completed" }
]);

// Log confirmation
print("MongoDB Initialization complete. Admin user and sample data created.");
