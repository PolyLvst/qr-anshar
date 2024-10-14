from flask import Flask,render_template,jsonify,request
from datetime import datetime
import json
import os
import sys
import colorama
from colorama import Fore

app = Flask(__name__)
colorama.init(autoreset=True)

now = datetime.now()
formatted_time = now.strftime("%d-%m-%Y")
# logger = write_some_log(f'./logs/{formatted_time}.log','db.py')
periodic_post = f"./db/post_periodic/post_periodic{formatted_time}.json"
# Imported from xlsx
import_json = f"./db/main.json"

def _get_cache_users():
    if os.path.exists(import_json):
        with open(import_json,"r") as f:
            return json.load(f)
    print(f"{Fore.RED}########## WARNING ##########")
    print(f"{Fore.RED}import from xlsx dapodik first [err empty students data]")
    return {}

cache:dict = _get_cache_users()

marked_students = []
if not os.path.exists("static/assets/student-pictures"):
    os.mkdir("static/assets/student-pictures")
if not os.path.exists("./db/post_periodic"):
    os.mkdir("./db/post_periodic")

def _get_student_info(id):
    try:
        results = cache[f"stu-id-{id}"]
        return results
    except Exception as e:
        # Id not found - {e}
        return None
    
print(f"{Fore.CYAN}>> Loaded students : {len(cache)}")
print(f"{Fore.CYAN}>> Consume : {sys.getsizeof(cache)} Bytes")
print(f"{Fore.CYAN}>> In memory cache ready ...")

@app.route("/",methods=["GET"])
def main():
    return render_template("index.html")

@app.route("/api/getid/<id>",methods=["GET"])
def get_name(id):
    results:dict = _get_student_info(id)
    if results == None:
        return jsonify({"status":"failed","msg":"failed, no student with that id"})
    data = {
        "data":{"name":results.get("nama")},
        "status":"oke",
        "msg":"success"
        }
    return jsonify(data)

@app.route("/api/absen",methods=["POST"])
def absen_siswa():
    nis = request.form.get("nis")
    results = _get_student_info(nis)
    if results == None:
        return jsonify({"status":"failed","msg":"Error, user id not found"})
    
    if nis in marked_students:
        return jsonify({"status":"failed","msg":"Siswa telah terabsen"})
    
    f_stu_id = f"stu-id-{nis}"
    lazy_upload = {}
    if os.path.exists(periodic_post):
        with open(periodic_post,'r') as f:
            lazy_upload = json.load(f)
        if f_stu_id in lazy_upload:
            # Already marked [post_periodic]
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

if __name__ == "__main__":
    # app.run("0.0.0.0",5000,True)
    port = 5000
    from waitress import serve
    serve(app, host='0.0.0.0', port=port)