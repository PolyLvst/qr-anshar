from flask import Flask,render_template,jsonify,request
from attendance_worker import lazy_attend_worker
from dotenv import load_dotenv
from datetime import datetime
from requests import Response
import threading
import requests
import sqlite3
import os
import re

app = Flask(__name__)

load_dotenv(override=True)
API_URL_ERINA_BASE = os.environ.get("API_URL_ERINA_BASE")

def get_db():
    conn = sqlite3.connect("attendance.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nis TEXT NOT NULL,
            student_id TEXT NOT NULL,
            student_name TEXT NOT NULL,
            class_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            is_sent TEXT NOT NULL DEFAULT 'no',
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def _get_cache_users():
    endpoint_users = f"{API_URL_ERINA_BASE}users"
    response:Response = requests.get(endpoint_users)
    if not response.ok:
        print(f"--- ERROR CANNOT GET {endpoint_users} ---")
        exit()
    data = response.json().get("values")
    info = {}
    # JSON
    for value in data:
        id = value.get("id")
        nis = value.get("name")
        full_name = value.get("full_name")
        c_id = value.get("class_id")
        info[f"stu-nis-{nis}"] = {"id":id, "nama":full_name,"class_id":c_id}
    return info

def _get_cache_class():
    endpoint_classes = f"{API_URL_ERINA_BASE}classes"
    response:Response = requests.get(endpoint_classes)
    if not response.ok:
        print(f"--- ERROR CANNOT GET {endpoint_classes} ---")
        exit()
    data = response.json().get("values")
    info = {}
    # JSON
    for value in data:
        id_c = value.get("id")
        c_name = value.get("class_name")
        info[f"class-id-{id_c}"] = {"id":id_c,"class_name":c_name}
    return info

cache:dict = _get_cache_users()
cache_class:dict = _get_cache_class()

if not os.path.exists("static/assets/student-pictures"):
    os.mkdir("static/assets/student-pictures")

def _get_student_info(nis):
    try:
        results = cache[f"stu-nis-{nis}"]
        return results
    except Exception as e:
        # Id not found - {e}
        return None
    
def _get_class_info(id):
    try:
        results = cache_class[f"class-id-{id}"]
        return results
    except Exception as e:
        # Id not found - {e}
        return None

# --- Startup --- #

def Startup():
    init_db()
    worker_thread = threading.Thread(target=lazy_attend_worker, daemon=True)
    worker_thread.start()

Startup()

# --- Startup --- #

@app.route("/",methods=["GET"])
def main():
    return render_template("index.html")

@app.route("/api/getid/<nis>",methods=["GET"])
def get_name(nis):
    results:dict = _get_student_info(nis)
    if results == None:
        return jsonify({"status":"failed","msg":"failed, no student with that id"})
    id_class = results.get("class_id")
    class_stu_unformat = _get_class_info(id_class).get("class_name")
    class_stu = re.sub(r"(?i)kelas", "", class_stu_unformat)
    data = {
        "data":{"name":results.get("nama"),
                "class":class_stu,
                "class_id":id_class,
                },
        "status":"oke",
        "msg":"success"
        }
    return jsonify(data)

@app.route("/api/absen", methods=["POST"])
def absen_siswa():
    nis = request.form.get("nis")
    if nis is None:
        # Unknown got none ...
        return jsonify({"status":"failed","msg":"Error, got None"})
    
    results = _get_student_info(nis)
    if results is None:
        return jsonify({"status": "failed", "msg": "Error, user id not found"})
    stu_id = results.get("id")
    class_id = results.get("class_id")
    stu_name = results.get("nama")

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%Y-%m-%d")

    conn = get_db()
    c = conn.cursor()

    # Check for duplicate entry
    c.execute("""
        SELECT 1 FROM attendance WHERE nis = ? AND date = ?
    """, (nis, current_date))
    if c.fetchone():
        conn.close()
        return jsonify({"status": "failed", "msg": "Siswa telah terabsen"})

    # Insert new attendance
    c.execute("""
        INSERT INTO attendance (nis, student_id, student_name, class_id, timestamp, is_sent, date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (nis, stu_id, stu_name, class_id, current_time, 'no', current_date))

    conn.commit()
    conn.close()

    return jsonify({"status": "oke", "msg": "success"})

@app.route("/api/absensi", methods=["GET"])
def view_attendance():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM attendance ORDER BY date DESC, timestamp DESC")
    rows = c.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

if __name__ == "__main__":
    # app.run("0.0.0.0",5000,True)
    port = 5000
    from waitress import serve
    serve(app, host='0.0.0.0', port=port)