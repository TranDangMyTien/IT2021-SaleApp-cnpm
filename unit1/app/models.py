from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime, Boolean, Time
from sqlalchemy.orm import relationship
from app import db
from flask_login import UserMixin
import enum
from datetime import datetime


# Chia role
class UserRoleEnum(enum.Enum):
    USER = 1
    EMPLOYEE = 2
    ADMIN = 3

# Tạo model chung
class BaseModel(db.Model):
    # Kích hoạt trừu tượng để nó không tạo thêm model
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    # Mặc định là lấy thời gian hiện tại bỏ vào
    # created_date = Column(DateTime, default=datetime.now())
    # active = Column(Boolean, default=True)


# Tài khoản
class Account(BaseModel, UserMixin):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(200), default = 'https://cdn.icon-icons.com/icons2/632/PNG/512/user_icon-icons.com_57997.png' )
    # Mặc định là tài khoản của khách hàng
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)

    # Phần relationship

    customer = relationship("Customer", uselist=False, backref="account")
    employee = relationship("Employee", uselist=False, backref="account")
    admin = relationship("Admin", uselist=False, backref="account")
    comments = relationship('Comment', backref='account', lazy=True)


    def __str__(self):
        return self.name

# Khách hàng
class Customer(db.Model):
    __tablename__ = 'customer'

    id_customer = Column(Integer, ForeignKey(Account.id), primary_key=True, autoincrement=True)
    name_customer = Column(String(50), nullable=False)
    cccd = Column(String(12), nullable=False, unique=True)
    sdt_customer = Column(String(10), nullable=False)


    # Phần relationship
    # account = relationship("Account", back_populates="customer")
    flight_ticket = relationship('FlightTicket', backref='customer', lazy=True)
    receipts = relationship('Receipt', backref='customer', lazy=True)

# Nhân viên
class Employee(db.Model):
    __tablename__ = 'employee'

    id_employee = Column(Integer, ForeignKey(Account.id), primary_key=True, autoincrement=True)
    name_employee = Column(String(50), nullable=False)
    sdt_employee = Column(String(10), nullable=False)

    # account = relationship("Account", back_populates="employee")
    flight_ticket = relationship("FlightTicket", uselist=False, backref="employee")
    schedule = relationship("Schedule", uselist=False, backref="employee")
    receipt = relationship('Receipt', backref='employee3', lazy=True)

# Quản trị
class Admin(db.Model):
    __tablename__ = 'admin'

    id = Column(Integer, ForeignKey(Account.id), primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    regulation = relationship('Regulation', backref='admin', lazy=True)
    flight = relationship('Flight', backref='admin', lazy=True)
    route = relationship('Route', backref='admin', lazy=True)


# Quy định
class Regulation(db.Model):
    __tablename__ = 'regulation'
    id = Column(Integer, primary_key=True, autoincrement=True )
    airport_count = Column(Integer)
    max_flight_time = Column(Integer)
    min_flight_time = Column(Integer)
    max_stopover_time = Column(Integer)
    min_stopover_time = Column(Integer)
    GiaVe = Column(Float)
    SLVe = Column(Integer)
    ticket_sales_time = Column(Integer)
    ticket_booking_time = Column(Integer)
    id_admin = Column(Integer, ForeignKey(Admin.id))

    flight = relationship("Flight", backref="regulation")
    flightticket = relationship("FlightTicket", backref="regulation")


# Lịch chuyến bay
class Schedule(db.Model):
    __tablename__ = 'schedule'
    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime)
    employee_id = Column(Integer, ForeignKey(Employee.id_employee), nullable=False)

    flight = relationship('Flight', backref='schedule', lazy=True)

# Doanh thu
class Revenue(BaseModel):
    __tablename__ = 'revenue'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    flight_count = Column(Integer)
    rate = Column(Float)
    revenue = Column(Float)
    receipt = relationship("Receipt", backref="revenue")
    route = relationship("Route", backref="revenue")

# Chuyến bay
class Flight(db.Model):
    __tablename__ = 'flight'

    # autoincrement : Có nghĩa là tự động tăng
    id = Column(Integer, primary_key=True, autoincrement=True)
    # String ở đây là mang nghĩa varchar, unique là không cho trùng tên
    name = Column(String(50), nullable=False, unique=True)
    status = Column(String(50), nullable=False)
    SLVeHang1 = Column(Integer, nullable=False)
    SLVeHang2 = Column(Integer, nullable=False)
    created_date = Column(DateTime, default=datetime.now())

    id_schedule = Column(Integer, ForeignKey(Schedule.id))
    id_regulation = Column(Integer, ForeignKey(Regulation.id))
    id_admin = Column(Integer, ForeignKey(Admin.id), primary_key=True)
    id_revenue = Column(Integer, ForeignKey(Revenue.id), nullable=False)


    flighttickets = relationship('FlightTicket', backref='flight', lazy=True)

    # Hiển thị như drop box cho phần create ở FlightTicket
    def __str__(self):
        return self.name



# Vé chuyến bay
class FlightTicket(db.Model):
    __tablename__ = 'flightticket'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, default=0)
    image = Column(String(200), default='https://cdn.icon-icons.com/icons2/3565/PNG/512/transport_travel_flight_airplane_ticket_plane_icon_225382.png')
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)
    id_employee = Column(Integer, ForeignKey(Employee.id_employee), primary_key=True)
    id_cus = Column(Integer, ForeignKey(Customer.id_customer), primary_key=True)
    id_regulation = Column(Integer, ForeignKey(Regulation.id))

    receipt_details = relationship('ReceiptDetails', backref='flightticket', lazy=True)
    comments = relationship('Comment', backref='flightticket', lazy=True)
    # Một thuộc tính có 2 khóa ngoại thì backref phải khác tên
    def __str__(self):
        return self.name






# Lưu trữ hóa đơn
class Receipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cus = Column(Integer, ForeignKey(Customer.id_customer), primary_key=True, nullable=False)
    employee_id = Column(Integer, ForeignKey(Employee.id_employee), nullable=False)
    revenue_id = Column(Integer, ForeignKey(Revenue.id), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    receipt_details = relationship('ReceiptDetails', backref='receipt', lazy=True)

# Hóa đơn chi tiết
class ReceiptDetails(db.Model):
    __tablename__ = 'receiptdetails'
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)

    receipt_id = Column(Integer, ForeignKey(Receipt.id), primary_key=True, nullable=False)
    flightticket_id = Column(Integer, ForeignKey(FlightTicket.id), nullable=False)


class Airport(BaseModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_airport = Column(String(100))
    route = relationship("Route", uselist=False, backref="airport")

class Route(BaseModel):
    __tablename__ = 'route'

    id = Column(Integer, primary_key=True, autoincrement=True)
    departure_location = Column(String(50))
    arrival_location = Column(String(50))
    SLSBTrungGian = Column(Integer)
    # departure_time = Column(Time)
    # arrival_time = Column(Time)
    id_regulation = Column(Integer, ForeignKey(Regulation.id))
    id_airport = Column(Integer, ForeignKey(Airport.id))

    id_admin = Column(Integer, ForeignKey(Admin.id), primary_key=True)
    id_revenue = Column(Integer, ForeignKey(Revenue.id), nullable=False)





# Tương tác, bình luận trên sản phẩm nào
class Interaction(BaseModel):
    # Không tạo table nên cho trừ tượng
    __abstract__ = True
    # Bình luận trên sản phẩm nào
    flightticket_id = Column(Integer, ForeignKey(FlightTicket.id), nullable=False)
    # Ai là người bình luận
    user_id = Column(Integer, ForeignKey(Account.id), nullable=False)

class Comment(Interaction):
    content = Column(String(255), nullable=False)
    created_date = Column(DateTime, default=datetime.now())



if __name__ == "__main__":
    from app import app
    with app.app_context():
        db.drop_all()
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