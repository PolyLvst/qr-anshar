from flask import Flask,render_template,jsonify
import mysql.connector
from dotenv import load_dotenv
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

def connect_db():
    try:
        conn = mysql.connector.connect(**db_config)
    except Exception as e:
        print(f'{e} \n --- Error --- ')
        exit()
    cursor = conn.cursor()
    return cursor,conn

def _get_cache_users(curr):
    sql = "SELECT name,full_name,class_id FROM users"
    curr.execute(sql)
    data = curr.fetchall()
    return data

def _get_cache_class(curr):
    sql = "SELECT id,class_name FROM classes"
    curr.execute(sql)
    data = curr.fetchall()
    return data

@app.route("/",methods=["GET"])
def main():
    return render_template("index.html")

@app.route("/api/getid/<id>",methods=["GET"])
def get_name(id):
    # Ini akan berbentuk tuple (Name,Full_Name,id_class)
    try:
        results:tuple = [t_stu for t_stu in cache if t_stu[0] == id][0]
    except IndexError as e:
        print(f"Id not found - {e}")
        return jsonify({"msg":"failed, no student with that id"})
    print(results)
    class_stu_unformat = cache_class[results[2]-1][1]
    class_stu = re.sub(r'(?i)kelas', '', class_stu_unformat)
    print(class_stu)
    data = {
        "data":{"name":results[1],
                "class":class_stu,
                "img_path":"",
                "status":"terabsen"},
        "msg":"success"
        }
    return jsonify(data)

@app.route("/api/create",methods=["POST"])
def create_stu():
    pass

if __name__ == "__main__":
    cursor,conn = connect_db()
    cache:list = _get_cache_users(cursor)
    cache_class:list = _get_cache_class(cursor)
    # print(cache)
    app.run("localhost",5000,True)
    cursor.close()
    conn.close()