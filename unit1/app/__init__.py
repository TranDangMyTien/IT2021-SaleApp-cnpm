#Phần có sẵn khi tạo packet app
#Phần cứng
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#Dòng này tạo một instance của class Flask và gán cho biến app.
#Biến __name__ là một biến đặc biệt trong Python và đại diện cho tên của module hiện tại.
app = Flask(__name__)
app.secret_key = 'jaoiuas8902BILbkjb###AKHBK'
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:m1234567890@localhost/saledbv1?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
#Cấu hình 1 trang có 6 sản phẩm
app.config["PAGE_SIZE"] = 6

db = SQLAlchemy(app=app)
login = LoginManager(app=app)


# Phần cloudinary
import cloudinary

cloudinary.config(
    cloud_name="dvxzmwuat",
    api_key="814652831379359",
    api_secret="BzgebW7M-yEgHzKWgEf176-MK6I"
)
