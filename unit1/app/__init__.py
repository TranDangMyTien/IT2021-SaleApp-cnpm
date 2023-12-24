#Phần có sẵn khi tạo packet app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#Dòng này tạo một instance của class Flask và gán cho biến app.
#Biến __name__ là một biến đặc biệt trong Python và đại diện cho tên của module hiện tại.
app = Flask(__name__)
app.secret_key = 'jaoiuas8902BILbkjb###AKHBK'
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:m1234567890@localhost/saledbv1?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)
login = LoginManager(app=app)