from flask import Flask,render_template,jsonify,request
from dotenv import load_dotenv
from datetime import datetime, timedelta
from requests import Response
import requests
import json
import os
import re

app = Flask(__name__)

load_dotenv(override=True)
API_URL_BASE = os.environ.get("API_URL_BASE")

now = datetime.now()
formatted_time = now.strftime("%d-%m-%Y")
# logger = write_some_log(f'./logs/{formatted_time}.log','db.py')
periodic_post = f"./db/post_periodic/post_periodic{formatted_time}.json"

def _get_cache_users():
    endpoint_users = f"{API_URL_BASE}api/users/"
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
    endpoint_classes = f"{API_URL_BASE}api/classes/"
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

marked_students = []
if not os.path.exists("static/assets/student-pictures"):
    os.mkdir("static/assets/student-pictures")
if not os.path.exists("./db/post_periodic"):
    os.mkdir("./db/post_periodic")

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

@app.route("/api/absen",methods=["POST"])
def absen_siswa():
    nis = request.form.get("nis")
    if nis == None:
        # Unknown got none ...
        return jsonify({"status":"failed","msg":"Error, got None"})
    
    results = _get_student_info(nis)
    stu_id = results.get("id")
    if results == None:
        return jsonify({"status":"failed","msg":"Error, user id not found"})
    
    if nis in marked_students:
        return jsonify({"status":"failed","msg":"Siswa telah terabsen"})
    
    f_stu_nis = f"stu-nis-{nis}"
    lazy_upload = {}
    if os.path.exists(periodic_post):
        with open(periodic_post,'r') as f:
            lazy_upload = json.load(f)
        if f_stu_nis in lazy_upload:
            # Already marked [post_periodic]
            return jsonify({"status":"failed","msg":"Siswa telah terabsen"})
        
    current_time = datetime.now().time()
    # Format the time as HH:MM:SS
    formatted_time_H_M_S = current_time.strftime("%H:%M:%S")

    with open(periodic_post,'w') as f:
        lazy_upload[f"{f_stu_nis}"]={"id":stu_id,"tipe":"HADIR","time":formatted_time_H_M_S}
        json.dump(lazy_upload,f)
        # logger.Log_write('Post_periodic updated')
    marked_students.append(nis)
    data = {
        "data":"data",
        "status":"oke",
        "msg":"success"}
    return jsonify(data)

if __name__ == "__main__":
    # app.run("0.0.0.0",5000,True)
    port = 5000
    from waitress import serve
    serve(app, host='0.0.0.0', port=port)