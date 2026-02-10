from flask import Flask, jsonify, request, send_from_directory
import sqlite3

app = Flask(__name__, static_folder='frontend')
DB_FILE = 'hrportal.db'

def init_db():
    db = sqlite3.connect(DB_FILE)
    db.execute('''CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        department TEXT NOT NULL,
        position TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    db.execute("INSERT OR IGNORE INTO employees (id, name, email, department, position) VALUES (1, 'John Doe', 'john.doe@company.com', 'Engineering', 'Software Engineer')")
    db.execute("INSERT OR IGNORE INTO employees (id, name, email, department, position) VALUES (2, 'Jane Smith', 'jane.smith@company.com', 'HR', 'HR Manager')")
    db.commit()
    db.close()

def get_db():
    db = sqlite3.connect(DB_FILE)
    db.row_factory = sqlite3.Row
    return db

@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

@app.route('/api/employees', methods=['GET'])
def get_employees():
    db = get_db()
    cursor = db.execute('SELECT * FROM employees')
    employees = [dict(row) for row in cursor.fetchall()]
    db.close()
    return jsonify(employees)

@app.route('/api/employees', methods=['POST'])
def add_employee():
    data = request.json
    db = get_db()
    cursor = db.execute(
        'INSERT INTO employees (name, email, department, position) VALUES (?, ?, ?, ?)',
        (data['name'], data['email'], data['department'], data['position'])
    )
    db.commit()
    employee_id = cursor.lastrowid
    db.close()
    return jsonify({'id': employee_id}), 201

@app.route('/api/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    db = get_db()
    db.execute('DELETE FROM employees WHERE id = ?', (id,))
    db.commit()
    db.close()
    return '', 204

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
