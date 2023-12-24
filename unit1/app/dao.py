from app.models import Category, Product, User
def load_categories():
    return Category.query.all()


# Hàm liệt kê các sản phẩm
def load_products(kw=None):
 products = Product.query
 if kw:
     products = products.filter(Product.name.contains(kw))
 return products.all()


def get_user_by_id(id):
    return User.query.get(id)