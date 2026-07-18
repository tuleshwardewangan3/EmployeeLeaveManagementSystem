from flask import Flask, jsonify, request
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

@app.route("/")
def home():
    return jsonify({
        "message": "Employee Leave Management System API is running"
    })

@app.route("/employees", methods=["GET"])
def get_employees():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(employees)

@app.route("/leave", methods=["POST"])
def apply_leave():
    data = request.get_json()

    connection = get_db_connection()
    cursor = connection.cursor()

    sql = """
        INSERT INTO leaves
        (employee_id, from_date, to_date, reason, status)
        VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        data["employee_id"],
        data["from_date"],
        data["to_date"],
        data["reason"],
        "Pending"
    )

    cursor.execute(sql, values)
    connection.commit()

    leave_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Leave application submitted successfully",
        "leave_id": leave_id
    }), 201

@app.route("/leaves", methods=["GET"])
def get_leaves():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            leaves.id,
            employees.name AS employee_name,
            leaves.from_date,
            leaves.to_date,
            leaves.reason,
            leaves.status
        FROM leaves
        JOIN employees
        ON leaves.employee_id = employees.id
    """)

    leaves = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(leaves)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)