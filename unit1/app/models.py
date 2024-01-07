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
    # flight_ticket = relationship('FlightTicket', backref='customer', lazy=True)
    receipts = relationship('Receipt', backref='customer', lazy=True)

# Nhân viên
class Employee(db.Model):
    __tablename__ = 'employee'

    id_employee = Column(Integer, ForeignKey(Account.id), primary_key=True, autoincrement=True)
    name_employee = Column(String(50), nullable=False)
    sdt_employee = Column(String(10), nullable=False, unique=True )

    # account = relationship("Account", back_populates="employee")
    # flight_ticket = relationship("FlightTicket", uselist=False, backref="employee")
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
    revenue = relationship('Revenue', backref='admin', lazy=True)

# Quy định
class Regulation(db.Model):
    __tablename__ = 'regulation'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False )
    airport_count = Column(Integer, nullable=False)
    max_flight_time = Column(Integer, nullable=False)
    min_flight_time = Column(Integer, nullable=False)
    max_stopover_time = Column(Integer, nullable=False)
    min_stopover_time = Column(Integer, nullable=False)
    GiaVe = Column(Float, nullable=False)
    SLVe = Column(Integer, nullable=False)
    ticket_sales_time = Column(Time, default=datetime.now(), nullable=False)
    ticket_booking_time = Column(Time, default=datetime.now(), nullable=False)
    id_admin = Column(Integer, ForeignKey(Admin.id))

    flight = relationship("Flight", backref="regulation")
    flightticket = relationship("FlightTicket", backref="regulation")


# Lịch chuyến bay
class Schedule(db.Model):
    __tablename__ = 'schedule'
    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime, default=datetime.now(), nullable=False)
    employee_id = Column(Integer, ForeignKey(Employee.id_employee), nullable=False)

    flight = relationship('Flight', backref='schedule', lazy=True)

# Doanh thu
class Revenue(BaseModel):
    __tablename__ = 'revenue'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    flight_count = Column(Integer, nullable=False)
    rate = Column(Float, nullable=False)
    id_admin = Column(Integer, ForeignKey(Admin.id))
    # revenue = Column(Float)
    receipt_details = relationship("ReceiptDetails", backref="revenue")
    route = relationship("Route", backref="revenue")
    flight = relationship("Flight", backref="revenue")


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
    created_date = Column(DateTime, default=datetime.now(), nullable=False)

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
    # id_employee = Column(Integer, ForeignKey(Employee.id_employee), primary_key=True)
    # id_cus = Column(Integer, ForeignKey(Customer.id_customer), primary_key=True)
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
    created_date = Column(DateTime, default=datetime.now())
    receipt_details = relationship('ReceiptDetails', backref='receipt', lazy=True)

# Hóa đơn chi tiết
class ReceiptDetails(db.Model):
    __tablename__ = 'receiptdetails'
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    revenue_id = Column(Integer, ForeignKey(Revenue.id), nullable=False)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), primary_key=True, nullable=False)
    flightticket_id = Column(Integer, ForeignKey(FlightTicket.id), nullable=False)


class Airport(BaseModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_airport = Column(String(100), nullable=False)
    route = relationship("Route", uselist=False, backref="airport")

class Route(BaseModel):
    __tablename__ = 'route'

    id = Column(Integer, primary_key=True, autoincrement=True)
    departure_location = Column(String(50), nullable=False)
    arrival_location = Column(String(50), nullable=False)
    SLSBTrungGian = Column(Integer, nullable=False)
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
        # db.drop_all()
        db.create_all()

        # import hashlib
        # u = Account(name='admin',
        #         username='admin',
        #         password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #         user_role=UserRoleEnum.ADMIN)
        # db.session.add(u)
        # u1 = Account(name='user',
        #             username='user1',
        #             password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #             user_role=UserRoleEnum.USER)
        # db.session.add(u1)
        # u2 = Account(name='employee',
        #             username='employee',
        #             password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #             user_role=UserRoleEnum.EMPLOYEE)
        # db.session.add(u2)
        # u3 = Account(name='KH2',
        #             username='khachhang2',
        #             password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #             user_role=UserRoleEnum.USER)
        # db.session.add(u3)
        # u4 = Account(name='KH3',
        #             username='khachhang3',
        #             password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #             user_role=UserRoleEnum.USER)
        # db.session.add(u4)
        # u5 = Account(name='admin',
        #         username='admin1',
        #         password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #         user_role=UserRoleEnum.ADMIN)
        # db.session.add(u5)
        # u6 = Account(name='employee',
        #             username='employee1',
        #             password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #             user_role=UserRoleEnum.EMPLOYEE)
        # db.session.add(u6)
        # db.session.commit()


        # a = Admin(id=1,name='Emma')
        # db.session.add(a)
        # db.session.commit()
        # a1 = Admin(id=6, name='Mie')
        # db.session.add(a1)
        # db.session.commit()

        # c = Customer(id_customer=2, name_customer='Nhi', cccd='092303005600', sdt_customer='0395129019')
        # c1 = Customer(id_customer=4, name_customer='Hien', cccd='092303005000', sdt_customer='0395129000')
        # c2 = Customer(id_customer=5, name_customer='Yen', cccd='092303005555', sdt_customer='0395129111')
        # db.session.add(c)
        # db.session.add(c1)
        # db.session.add(c2)
        # db.session.commit()

        # e = Employee(id_employee=3, name_employee='Linh', sdt_employee='0899484111')
        # e1 = Employee(id_employee=7, name_employee='Nga', sdt_employee='0899484000')
        # db.session.add(e)
        # db.session.add(e1)
        # db.session.commit()


        # r = Revenue(name='Thang1', flight_count=20, rate={15/100}, id_admin=6 )
        # r1 = Revenue(name='Thang2', flight_count=50, rate={19/100}, id_admin=6 )
        # db.session.add(r)
        # db.session.add(r1)
        # db.session.commit()


        # r = Regulation(id=1, airport_count=5, max_flight_time=5, min_flight_time=1, max_stopover_time=1, min_stopover_time=0, GiaVe=1000000, SLVe=1000, ticket_sales_time="8:30:00", ticket_booking_time="8:30:00", id_admin=1)
        # r1 = Regulation(id=2, airport_count=10, max_flight_time=10, min_flight_time=1, max_stopover_time=1, min_stopover_time=0, GiaVe=800000, SLVe=1200, ticket_sales_time="8:30:00", ticket_booking_time="8:30:00", id_admin=6)
        # db.session.add(r)
        # db.session.add(r1)
        # db.session.commit()


        # s = Schedule(id=1, datetime="2024-02-07 12:30:00", employee_id=3)
        # s1 = Schedule(id=2, datetime="2024-02-05 8:00:00", employee_id=3)
        # db.session.add(s)
        # db.session.add(s1)
        # db.session.commit()

        # c1 = Flight(name='HN-SG', status="proceed", SLVeHang1=50, SLVeHang2=10, created_date="2024-01-07 12:30:00", id_schedule=1, id_regulation=1, id_admin=1, id_revenue=1)
        # c2 = Flight(name='HN-CT', status="waiting", SLVeHang1=100, SLVeHang2=30, created_date="2024-03-02 10:00:00", id_schedule=1, id_regulation=1, id_admin=1, id_revenue=1)
        # c3 = Flight(name='HN-ST', status="cancel", SLVeHang1=100, SLVeHang2=100, created_date="2024-02-01 12:00:00", id_schedule=1, id_regulation=1, id_admin=1, id_revenue=1)
        # c4 = Flight(name='CT-DL', status="cancel", SLVeHang1=100, SLVeHang2=30, created_date="2023-12-01 2:30:00", id_schedule=1, id_regulation=1, id_admin=1, id_revenue=1)
        # c5 = Flight(name='CT-HN', status="waiting", SLVeHang1=60, SLVeHang2=30, created_date="2024-02-11 1:30:00", id_schedule=1, id_regulation=1, id_admin=1, id_revenue=1)
        # c6 = Flight(name='CT-SG', status="waiting", SLVeHang1=60, SLVeHang2=20, created_date="2024-02-02 12:30:00", id_schedule=1, id_regulation=1, id_admin=1, id_revenue=1)
        # db.session.add(c1)
        # db.session.add(c2)
        # db.session.add(c3)
        # db.session.add(c4)
        # db.session.add(c5)
        # db.session.add(c6)
        # db.session.commit()



        # l = FlightTicket(id=1, name='HN-SG', price=2680000, image='https://images.pexels.com/photos/414110/pexels-photo-414110.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', flight_id=1, id_regulation=1)
        # l1 = FlightTicket(id=2, name='HN-CT', price=2000000, image='https://images.pexels.com/photos/169647/pexels-photo-169647.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', flight_id=2, id_regulation=1)
        # l2 = FlightTicket(id=3, name='HN-CT', price=1500000, image='https://images.pexels.com/photos/169647/pexels-photo-169647.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', flight_id=2, id_regulation=1)
        # l3 = FlightTicket(id=4, name='HN-ST', price=3500000, image='https://images.pexels.com/photos/1004665/pexels-photo-1004665.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', flight_id=3, id_regulation=1)
        # l4 = FlightTicket(id=5, name='CT-DL', price=2000000, image='https://images.pexels.com/photos/1470405/pexels-photo-1470405.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', flight_id=4, id_regulation=1)
        # db.session.add(l)
        # db.session.add(l1)
        # db.session.add(l2)
        # db.session.add(l3)
        # db.session.add(l4)
        # db.session.commit()