from flask import Flask, jsonify, request

app = Flask(__name__)

employees = [
    {"id": 1, "name": "Amit", "department": "IT"},
    {"id": 2, "name": "Priya", "department": "HR"},
    {"id": 3, "name": "Rahul", "department": "Finance"}
]

leaves = []

@app.route("/")
def home():
    return jsonify({
        "message": "Employee Leave Management System API is running"
    })

@app.route("/employees", methods=["GET"])
def get_employees():
    return jsonify(employees)

@app.route("/leave", methods=["POST"])
def apply_leave():
    data = request.get_json()

    leave = {
        "id": len(leaves) + 1,
        "employee_id": data["employee_id"],
        "from_date": data["from_date"],
        "to_date": data["to_date"],
        "reason": data["reason"],
        "status": "Pending"
    }

    leaves.append(leave)

    return jsonify({
        "message": "Leave application submitted successfully",
        "leave": leave
    }), 201

@app.route("/leaves", methods=["GET"])
def get_leaves():
    return jsonify(leaves)

if __name__ == "__main__":
    app.run(debug=True)