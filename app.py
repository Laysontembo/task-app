from flask import Flask, request, jsonify

app = Flask(__name__)

# -----------------------------
# Fake database (memory)
# -----------------------------
tasks = []
next_id = 1


# -----------------------------
# GET ALL TASKS
# -----------------------------
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks), 200


# -----------------------------
# CREATE NEW TASK
# -----------------------------
@app.route('/tasks', methods=['POST'])
def create_task():
    global next_id
    data = request.get_json()

    # -------- VALIDATION --------
    if not data:
        return jsonify({"error": "Request body required"}), 400

    if "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    if "priority" in data:
        if data["priority"] not in ["Low", "Medium", "High"]:
            return jsonify({"error": "Priority must be Low, Medium, or High"}), 400

    # -------- CREATE TASK --------
    task = {
        "id": next_id,
        "title": data["title"],
        "due_date": data.get("due_date"),
        "priority": data.get("priority", "Low")
    }

    tasks.append(task)
    next_id += 1

    return jsonify(task), 201


# -----------------------------
# SEARCH TASKS
# -----------------------------
@app.route('/tasks/search', methods=['GET'])
def search_tasks():
    keyword = request.args.get("q")

    if not keyword:
        return jsonify({"error": "Search query required"}), 400

    results = [
        task for task in tasks
        if keyword.lower() in task["title"].lower()
    ]

    return jsonify(results), 200


# -----------------------------
# ADD TEST TASK (Browser Only)
# -----------------------------
@app.route('/add-test-task')
def add_test_task():
    global next_id

    task = {
        "id": next_id,
        "title": "Study Flask",
        "due_date": "2026-03-01",
        "priority": "High"
    }

    tasks.append(task)
    next_id += 1

    return jsonify(task)


# -----------------------------
# GLOBAL ERROR HANDLER
# -----------------------------
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)