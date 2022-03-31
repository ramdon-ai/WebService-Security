from flask import Flask, jsonify, request,make_response
import os, random, string
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "users.db"))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    token = db.Column(db.String(225), unique=True, nullable=True)
db.create_all()

@app.route('/api/register', methods=['POST'])
def daftar():
    dataUsername = request.form.get('username')
    dataPassword = request.form.get('password')
    
    if dataUsername and dataPassword:
        dataModel = User(username=dataUsername, password=dataPassword)
        db.session.add(dataModel)
        db.session.commit()
        return make_response(jsonify({"Msg ":"Register Berhasil"}), 200)
    return jsonify({"Msg ":"Username/Password harus diisi"})

@app.route('/api/v1/login', methods=['POST'])
def masuk():
    dataUsername = request.form.get('username')
    dataPassword = request.form.get('password')
    akun = User.query.filter_by(username=dataUsername, password=dataPassword).first()
    if akun:
        dataToken = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        User.query.filter_by(username=dataUsername, password=dataPassword).update({'token': dataToken})
        db.session.commit()
        return make_response(jsonify({"Token API":dataToken}),200)
    return jsonify({"msg":"Mengambil Info Token Gagal"}) 

@app.route('/api/v2/users/info', methods=['POST'])
def info_pengguna():
    dataToken = request.values.get('token')
    akun = User.query.filter_by(token=dataToken).first()
    if akun:
        return akun.username 
    else:
        return 'Token yang anda masukkan salah'
        
if __name__ == '__main__':
    app.run(debug=True, port=4000)