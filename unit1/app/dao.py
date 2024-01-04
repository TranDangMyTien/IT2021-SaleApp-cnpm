from app.models import Category, Product, User
from app import app, db
import hashlib


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
