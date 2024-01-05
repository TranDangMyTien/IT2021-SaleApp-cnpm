from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime, Boolean
from sqlalchemy.orm import relationship
from app import db
from flask_login import UserMixin
import enum
from datetime import datetime


# Chia role
class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2
    MANAGER = 3

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avartar = Column(String(200), default = 'https://images.pexels.com/photos/19140963/pexels-photo-19140963/free-photo-of-m-c-h-du-l-ch-n-c-d-c.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2' )
    # Mặc định là tài khoản của khách hàng
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Category(db.Model):
    __tablename__ = 'category'

    # autoincrement : Có nghĩa là tự động tăng
    id = Column(Integer, primary_key=True, autoincrement=True)
    # String ở đây là mang nghĩa varchar, unique là không cho trùng tên
    name = Column(String(50), nullable=False, unique=True)
    products = relationship('Product', backref='category', lazy=True)

    # Hiển thị như drop box cho phần create ở Product
    def __str__(self):
        return self.name


class Product(db.Model):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, default=0)
    image = Column(String(200), default="https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242"
                                        "/hclq65mc6so7vdrbp7hz.jpg")
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='product', lazy=True)
    comments = relationship('Comment', backref='product', lazy=True)
    # Một thuộc tính có 2 khóa ngoại thì backref phải khác tên
    def __str__(self):
        return self.name

# Tạo model chung
class BaseModel(db.Model):
    # Kích hoạt trừu tượng để nó không tạo thêm model
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    # Mặc định là lấy thời gian hiện tại bỏ vào
    created_date = Column(DateTime, default=datetime.now())
    active = Column(Boolean, default=True)


# Lưu trữ hóa đơn
class Receipt(BaseModel):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='receipt', lazy=True)

# Hóa đơn chi tiết
class ReceiptDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)


# Tương tác, bình luận trên sản phẩm nào
class Interaction(BaseModel):
    # Không tạo table nên cho trừ tượng
    __abstract__ = True
    # Bình luận trên sản phẩm nào
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    # Ai là người bình luận
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)

class Comment(Interaction):
    content = Column(String(255), nullable=False)
    created_date = Column(DateTime, default=datetime.now())



if __name__ == "__main__":
    from app import app
    with app.app_context():
        db.create_all()
        # c1 = Category(name='Mobile')
        # c2 = Category(name='Table')
        # c3 = Category(name='Desktop')
        # c4 = Category(name='Phu kien')
        # db.session.add(c3)
        # db.session.add(c4)
        # db.session.add(c1)
        # db.session.add(c2)
        # db.session.commit()

        # p1 = Product(name='iPad Pro 2022', price=24000000, category_id=2)
        # p2 = Product(name='iPhone 14', price=25000000, category_id=1)
        # p3 = Product(name='Galaxy S23', price=24000000, category_id=1)
        # p4 = Product(name='Note 22', price=24000000, category_id=1)
        # p5 = Product(name='Galaxy Tab S9', price=24000000, category_id=2)
        # db.session.add_all([p1, p2, p3, p4, p5])
        # db.session.commit()
        #
        #
        #
        # import hashlib
        # u = User(name='admin',
        #         username='admin',
        #         password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #         user_role=UserRoleEnum.ADMIN)
        # db.session.add(u)
        # db.session.commit()

        # u1 = User(name='manager',
        #         username='manager',
        #         password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #         user_role=UserRoleEnum.MANAGER)
        #
        # db.session.add(u1)
        # db.session.commit()

        # u2 = User(name='user1',
        #         username='user1',
        #         password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #         user_role=UserRoleEnum.USER)
        #
        # db.session.add(u2)
        # db.session.commit()