from app.models import Flight, FlightTicket, Account, Receipt, ReceiptDetails, Comment
from app import app, db
import hashlib
import cloudinary.uploader
from flask_login import current_user
from sqlalchemy import func

def load_flights():
    return Flight.query.all()


# Hàm liệt kê các sản phẩm, tìm kiếm sản phẩm theo kw, tìm kiếm theo
def load_flighttickets(kw, flight_id, page=None):
    flighttickets = FlightTicket.query
    if kw:
     flighttickets = flighttickets.filter(FlightTicket.name.contains(kw))
    if flight_id:
     flighttickets = flighttickets.filter(FlightTicket.flight_id.__eq__(flight_id))
    if page:
        # Ép về kiểu số nguyên
        page = int(page)
        # Số lượng trang
        page_size = app.config['PAGE_SIZE']
        # Tính từ vị trí bắt đầu (0->...)
        start = (page - 1) * page_size
        return flighttickets.slice(start, start + page_size)
    return flighttickets.all()


# Hàm đếm số lượng sản phẩm
def count_flightticket():
    return FlightTicket.query.count()


def get_user_by_id(id):
    return Account.query.get(id)

# Xác thực đăng nhập, từ cái đã băm trở về ban đầu
# strip() cắt khoản trắng
def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return Account.query.filter(Account.username.__eq__(username.strip()),
                            Account.password.__eq__(password)).first()


# Hàm thêm user
def add_user(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = Account(name=name, username=username, password=password)
    if avatar:
        res = cloudinary.uploader.upload(avatar)
        print(res)
        # secure_url : URL đã upload lên cloud, lưu về máy
        u.avatar = res['secure_url']

    db.session.add(u)
    db.session.commit()


# Hàm thêm hóa đơn
def add_receipt(cart):
    if cart:
        r = Receipt(user=current_user)
        db.session.add(r)

        for c in cart.values():
            d = ReceiptDetails(quantity=c['quantity'], price=c['price'],
                               receipt=r, flightticket_id=c['id'])
            db.session.add(d)

        db.session.commit()

# Hàm đếm sồ FlightTicket có trong 1 Flight
# Như là câu truy vấn mySQL
def count_flighttickets_by_cate():
    return db.session.query(Flight.id, Flight.name, func.count(FlightTicket.id))\
                     .join(FlightTicket, FlightTicket.flight_id == Flight.id, isouter=True).group_by(Flight.id).all()
# isouter = True chỉ rằng đây là liên kết left outer join
# sẽ trả về tất cả các hàng từ bản bên trái (bảng chính: Flight)

# Thống kê doanh thu
def revenue_stats(kw=None):
    query = db.session.query(FlightTicket.id, FlightTicket.name, func.sum(ReceiptDetails.price*ReceiptDetails.quantity))\
                     .join(ReceiptDetails, ReceiptDetails.flightticket_id == FlightTicket.id).group_by(FlightTicket.id)
    if kw:
        query = query.filter(FlightTicket.name.contains(kw))

    return query


# Thống kê doanh thu theo tháng
def revenue_stats_by_month(year=2024):
    return db.session.query(func.extract('month', Receipt.created_date),
                            func.sum(ReceiptDetails.price*ReceiptDetails.quantity))\
                        .join(ReceiptDetails, ReceiptDetails.receipt_id == Receipt.id)\
                        .filter(func.extract('year', Receipt.created_date) == year)\
                        .group_by(func.extract('month', Receipt.created_date)).all()


# Lấy comment của 1 sản phẩm
def get_comments_by_prod_id(id):
    return Comment.query.filter(Comment.flightticket_id.__eq__(id)).all()

# Thêm comment
def add_comment(flightticket_id, content):
    c = Comment(user=current_user, flightticket_id=flightticket_id, content=content)
    db.session.add(c)
    db.session.commit()

    return c



# Lấy id của sản phẩm
def get_flightticket_by_id(id):
    return FlightTicket.query.get(id)

if __name__ == '__main__':
    with app.app_context():
        print(count_flighttickets_by_cate())


