from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avartar = Column(String(200), default = 'https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242"/hclq65mc6so7vdrbp7hz.jpg' )

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


if __name__ == "__main__":
    from app import app
    with app.app_context():
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

        # db.create_all()

        import hashlib
        u = User(name="Admin", username='admin', password=str(hashlib.md5('m1234567890'.encode('utf-8')).hexdigest()))
        db.session.add(u)
        db.session.commit()