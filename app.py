from flask import Flask,render_template,jsonify,request
from dotenv import load_dotenv
from datetime import datetime
import mysql.connector
import json
import os
import re

app = Flask(__name__)

load_dotenv()
HOST_DB = os.environ.get("HOST_DB")
USER_DB = os.environ.get("USER_DB")
PASS_DB = os.environ.get("PASS_DB")
NAME_DB = os.environ.get("NAME_DB")
db_config = {
    "host": HOST_DB,
    "user": USER_DB,
    "password": PASS_DB,
    "database": NAME_DB
}
now = datetime.now()
formatted_time = now.strftime("%d-%m-%Y")
# logger = write_some_log(f'./logs/{formatted_time}.log','db.py')
periodic_post = f"./db/post_periodic/post_periodic{formatted_time}.json"

def connect_db():
    try:
        conn = mysql.connector.connect(**db_config)
    except Exception as e:
        print(f"{e} \n --- Error --- ")
        exit()
    cursor = conn.cursor()
    return cursor,conn

def _get_cache_users(curr):
    sql = "SELECT name,full_name,class_id FROM users"
    curr.execute(sql)
    data = curr.fetchall()
    info = {}
    # JSON
    for row in data:
        id,full_name,c_id = row
        info[f"stu-id-{id}"] = {"nama":full_name,"class_id":c_id}
    return info

def _get_cache_class(curr):
    sql = "SELECT id,class_name FROM classes"
    curr.execute(sql)
    data = curr.fetchall()
    info = {}
    # JSON
    for row in data:
        id_c,c_name = row
        info[f"class-id-{id_c}"] = {"id":id_c,"class_name":c_name}
    return info

def _get_student_info(id):
    try:
        results = cache[f"stu-id-{id}"]
        return results
    except Exception as e:
        print(f"Id not found - {e}")
        return None

@app.route("/",methods=["GET"])
def main():
    return render_template("index.html")

@app.route("/api/getid/<id>",methods=["GET"])
def get_name(id):
    results:dict = _get_student_info(id)
    # print(results)
    if results == None:
        return jsonify({"status":"failed","msg":"failed, no student with that id"})
    id_class = results.get("class_id")
    class_stu_unformat = cache_class[f"class-id-{id_class}"].get("class_name")
    class_stu = re.sub(r"(?i)kelas", "", class_stu_unformat)
    # print(class_stu)
    data = {
        "data":{"name":results.get("nama"),
                "class":class_stu,
                "img_path":results.get("img_path"),},
        "status":"oke",
        "msg":"success"
        }
    return jsonify(data)

@app.route("/api/absen",methods=["POST"])
def absen_siswa():
    nis = request.form.get("nis")
    print(nis)
    if nis == None:
        print("Unknown got none ... ")
        return jsonify({"status":"failed","msg":"Error, got None"})
    
    results = _get_student_info(nis)
    if results == None:
        print("")
        return jsonify({"status":"failed","msg":"Error, user id not found"})
    
    if nis in marked_students:
        print("Already marked")
        return jsonify({"status":"failed","msg":"Siswa telah terabsen"})
    
    f_stu_id = f"stu-id-{nis}"
    lazy_upload = {}
    if os.path.exists(periodic_post):
        with open(periodic_post,'r') as f:
            lazy_upload = json.load(f)
        if f_stu_id in lazy_upload:
            print("Already marked [post_periodic]")
            return jsonify({"status":"failed","msg":"Siswa telah terabsen"})
        
    current_time = datetime.now().time()
    # Format the time as HH:MM:SS
    formatted_time_H_M_S = current_time.strftime("%H:%M:%S")

    with open(periodic_post,'w') as f:
        lazy_upload[f"{f_stu_id}"]={"id":nis,"tipe":"HADIR","time":formatted_time_H_M_S}
        json.dump(lazy_upload,f)
        # logger.Log_write('Post_periodic updated')
    marked_students.append(nis)
    data = {
        "data":"data",
        "status":"oke",
        "msg":"success"}
    return jsonify(data)

@app.route("/api/create",methods=["POST"])
def create_stu():
    pass

if __name__ == "__main__":
    cursor,conn = connect_db()
    cache:dict = _get_cache_users(cursor)
    cache_class:dict = _get_cache_class(cursor)
    cursor.close()
    conn.close()
    
    marked_students = []
    app.run("localhost",5000,True)