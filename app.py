import secrets
from PIL import Image
from flask import Flask,render_template,jsonify,request
from dotenv import load_dotenv
from datetime import datetime, timedelta
import mysql.connector
import json
import jwt
import os
import re

app = Flask(__name__)

load_dotenv(override=True)
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
SECRET_KEY = os.environ.get("SECRET_KEY")
TOKEN = os.environ.get("TOKEN")
ALGORITHM = os.environ.get("ALGORITHM")
ADMIN_NM = os.environ.get("ADMIN_NM")
ADMIN_PW = os.environ.get("ADMIN_PW")
# JWT Token exp
Expired_Seconds = 60 * 60 * 24 # 24 Hour / 86400 seconds

now = datetime.now()
formatted_time = now.strftime("%d-%m-%Y")
# logger = write_some_log(f'./logs/{formatted_time}.log','db.py')
periodic_post = f"./db/post_periodic/post_periodic{formatted_time}.json"
allowed_ext = {'png', 'jpg', 'jpeg'}

def connect_db():
    try:
        conn = mysql.connector.connect(**db_config)
    except Exception as e:
        print(f"{e} \n --- Error --- ")
        exit()
    cursor = conn.cursor()
    return cursor,conn

def not_allowed_file(filename:str):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_ext

def _get_cache_users(curr):
    sql = "SELECT id,name,full_name,class_id FROM users"
    curr.execute(sql)
    data = curr.fetchall()
    info = {}
    # JSON
    for row in data:
        id,nis,full_name,c_id = row
        info[f"stu-nis-{nis}"] = {"id":id, "nama":full_name,"class_id":c_id}
    return info

def _get_cache_class(curr):
    # sql = "SELECT id,class_name FROM classes ORDER BY classes.class_name ASC"
    sql = "SELECT id,class_name FROM classes"
    curr.execute(sql)
    data = curr.fetchall()
    info = {}
    # JSON
    for row in data:
        id_c,c_name = row
        info[f"class-id-{id_c}"] = {"id":id_c,"class_name":c_name}
    return info

cursor,conn = connect_db()
cache:dict = _get_cache_users(cursor)
cache_class:dict = _get_cache_class(cursor)
cursor.close()
conn.close()

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

@app.route("/api/get_classrooms",methods=["GET"])
def get_classrooms():
    data_list = [{"class_name": item["class_name"], "id": item["id"]} for item in cache_class.values()]
    return jsonify({"data":data_list})

@app.route("/api/getid/<nis>",methods=["GET"])
def get_name(nis):
    results:dict = _get_student_info(nis)
    if results == None:
        return jsonify({"status":"failed","msg":"failed, no student with that id"})
    id_class = results.get("class_id")
    class_stu_unformat = cache_class[f"class-id-{id_class}"].get("class_name")
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

@app.route("/api/add_student",methods=["POST"])
def create_stu():
    token_receive = request.cookies.get(TOKEN)
    try:
        payload = jwt.decode(token_receive,SECRET_KEY,algorithms=[ALGORITHM])
        msg = "token is valid, Authenticated"
        pass
    except jwt.ExpiredSignatureError:
        msg = 'Your session has expired'
        return jsonify({"msg":msg,"status":"not authenticated"})
    except jwt.exceptions.DecodeError:
        msg = 'Something wrong happens'
        return jsonify({"msg":msg,"status":"not authenticated"})
    
    curr,conn = connect_db()
    nis = request.form.get("nis")
    nama = request.form.get("nama")
    kelas = request.form.get("kelas")
    if not nis or not nama or not kelas:
        return jsonify({"status":"failed","msg":"data incomplete"})
    
    is_user_exist = _get_student_info(nis)
    if is_user_exist:
        return jsonify({"status":"failed","msg":"ID terpakai"})
    
    is_class_exist = _get_class_info(kelas)
    if not is_class_exist:
        return jsonify({"status":"failed","msg":"Kelas tidak ditemukan"})
    
    if "file" in request.files:
        image_receive = request.files.get("file")
        if not_allowed_file(image_receive):
            return jsonify({"status":"failed","msg":f"Extensions allowed : {allowed_ext}"})

        # extension = image_receive.filename.split('.')[-1]
        extension = "jpg"
        file_name_image = f'static/assets/student-pictures/{nis}.{extension}'
        image = Image.open(image_receive)
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        image.save(os.path.join(app.root_path,file_name_image),format='JPEG')
        # path_img = file_name_image
        insert_query = """
            INSERT INTO users (name, full_name, class_id)
            VALUES (%s, %s, %s)
        """
        curr.execute(insert_query,(nis,nama,kelas))
        generated_id = curr.lastrowid
        conn.commit()
        curr.close()
        conn.close()
        # Update in memory cache
        cache[f"stu-nis-{nis}"] = {"id":generated_id,"nama":nama,"class_id":kelas}
        return jsonify({"status":"success","msg":"Siswa berhasil terdaftar"})
    else:
        return jsonify({"status":"failed","msg":"Foto tidak terupload"})
    
@app.route("/api/edit_student",methods=["POST"])
def edit_stu():
    token_receive = request.cookies.get(TOKEN)
    try:
        payload = jwt.decode(token_receive,SECRET_KEY,algorithms=[ALGORITHM])
        msg = "token is valid, Authenticated"
        pass
    except jwt.ExpiredSignatureError:
        msg = 'Your session has expired'
        return jsonify({"msg":msg,"status":"not authenticated"})
    except jwt.exceptions.DecodeError:
        msg = 'Something wrong happens'
        return jsonify({"msg":msg,"status":"not authenticated"})
    
    curr,conn = connect_db()
    nis = request.form.get("nis")
    nama = request.form.get("nama")
    kelas = request.form.get("kelas")
    if not nis or not nama or not kelas:
        return jsonify({"status":"failed","msg":"data incomplete"})
    
    is_user_exist = _get_student_info(nis)
    if not is_user_exist:
        return jsonify({"status":"failed","msg":"ID tidak ditemukan"})
    
    is_class_exist = _get_class_info(kelas)
    if not is_class_exist:
        return jsonify({"status":"failed","msg":"Kelas tidak ditemukan"})
    insert_query = """
        UPDATE users SET name = %s, full_name = %s, class_id=%s WHERE name = %s
    """
    curr.execute(insert_query,(nis,nama,kelas,nis))
    conn.commit()
    curr.close()
    conn.close()
    # Update in memory cache
    previous_id = is_user_exist.get("id")
    cache[f"stu-nis-{nis}"] = {"id":previous_id,"nama":nama,"class_id":kelas}
    if "file" in request.files:
        image_receive = request.files.get("file")
        if not_allowed_file(image_receive):
            return jsonify({"status":"failed","msg":f"Extensions allowed : {allowed_ext}"})

        # extension = image_receive.filename.split('.')[-1]
        extension = "jpg"
        file_name_image = f'static/assets/student-pictures/{nis}.{extension}'
        image = Image.open(image_receive)
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        image.save(os.path.join(app.root_path,file_name_image),format='JPEG')
        # path_img = file_name_image
        return jsonify({"status":"success","msg":"Data terupdate"})
    else:
        return jsonify({"status":"success","msg":"Data terupdate"})

@app.route('/sign_in',methods=['POST'])
def sign_in():
    username_receive = request.form.get('username_give')
    password_receive = request.form.get('password_give')
    is_correct_username = secrets.compare_digest(ADMIN_NM,username_receive)
    is_correct_password = secrets.compare_digest(ADMIN_PW,password_receive)
    if not is_correct_username or not is_correct_password:
        return jsonify({"result": "fail","msg": "Cannot find user with that combination of id and password",})
    payload = {
        "id": username_receive,
        "exp": datetime.utcnow() + timedelta(seconds=Expired_Seconds),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return jsonify({"result": "success","token": token})

if __name__ == "__main__":
    # app.run("0.0.0.0",5000,True)
    port = 5000
    from waitress import serve
    serve(app, host='0.0.0.0', port=port)