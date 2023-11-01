from flask import Flask,render_template,jsonify
import os

app = Flask(__name__)

@app.route("/",methods=["GET"])
def main():
    return render_template("index.html")

@app.route("/api/getid/<id>",methods=["GET"])
def getName(id):
    dir_path = "static/assets/student-pictures"
    file_name = id
    file_path = os.path.join(dir_path,file_name)
    if os.path.isfile(file_path):
        file_extension = os.path.splitext(file_path)[1]
        print(file_path,file_extension)
    else:
        print("Not found")
    data = {
        "data":{"name":"Test",
                "class":"12"},
        "msg":"success"
        }
    return jsonify(data)

if __name__ == "__main__":
    app.run("localhost",5000,True)