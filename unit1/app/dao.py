from app.models import Category, Product, User, Receipt, ReceiptDetails, Comment
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

# Hàm đếm sồ Product có trong 1 Category
# Như là câu truy vấn mySQL
def count_products_by_cate():
    return db.session.query(Category.id, Category.name, func.count(Product.id))\
                     .join(Product, Product.category_id == Category.id, isouter=True).group_by(Category.id).all()
# isouter = True chỉ rằng đây là liên kết left outer join
# sẽ trả về tất cả các hàng từ bản bên trái (bảng chính: Category)

# Thống kê doanh thu
def revenue_stats(kw=None):
    query = db.session.query(Product.id, Product.name, func.sum(ReceiptDetails.price*ReceiptDetails.quantity))\
                     .join(ReceiptDetails, ReceiptDetails.product_id == Product.id).group_by(Product.id)
    if kw:
        query = query.filter(Product.name.contains(kw))

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
    return Comment.query.filter(Comment.product_id.__eq__(id)).all()

# Thêm comment
def add_comment(product_id, content):
    c = Comment(user=current_user, product_id=product_id, content=content)
    db.session.add(c)
    db.session.commit()

    return c



# Lấy id của sản phẩm
def get_product_by_id(id):
    return Product.query.get(id)

if __name__ == '__main__':
    with app.app_context():
        print(count_products_by_cate())


