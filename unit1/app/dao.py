from app.models import Category, Product, User, Receipt, ReceiptDetails
from app import app, db
import hashlib
import cloudinary.uploader
from flask_login import current_user
from sqlalchemy import func

def load_categories():
    return Category.query.all()


# Hàm liệt kê các sản phẩm, tìm kiếm sản phẩm theo kw, tìm kiếm theo
def load_products(kw=None, cate_id=None, page = None):
 products = Product.query
 if kw:
     products = products.filter(Product.name.contains(kw))
 if cate_id:
     products = products.filter(Product.category_id.__eq__(cate_id))
 if page:
        # Ép về kiểu số nguyên
        page = int(page)
        # Số lượng trang
        page_size = app.config['PAGE_SIZE']
        # Tính từ vị trí bắt đầu (0->...)
        start = (page - 1) * page_size
        return products.slice(start, start + page_size)
 return products.all()


# Hàm đếm số lượng sản phẩm
def count_product():
    return Product.query.count()


def get_user_by_id(id):
    return User.query.get(id)

# Xác thực đăng nhập, từ cái đã băm trở về ban đầu
# strip() cắt khoản trắng
def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                            User.password.__eq__(password)).first()


# Hàm thêm user
def add_user(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name, username=username, password=password)
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
                               receipt=r, product_id=c['id'])
            db.session.add(d)

        db.session.commit()