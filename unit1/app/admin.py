from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose, AdminIndexView
from app import app, db, dao
from app.models import Category, Product
from flask_login import logout_user, current_user
from flask import redirect, request
from app.models import UserRoleEnum


# class MyAdminIndex(AdminIndexView):
#     @expose('/')
#     def index(self):
#         return self.render('admin/index.html', stats=dao.count_products_by_cate())

# Tạo lớp chứng thực tài khoản thì mới thấy tab nào đó
class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

# Tạo lớp chứng thực cho kiểu Model, và nó là role Admin
class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN

class AuthenticatedManager(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.MANAGER


# MyProductView kế thừa lại ModelView
class MyProductView(AuthenticatedAdmin):
    # Tab Product (trong trang admin) : chỉ hiện những cột dưới
    column_list = ['id', 'name', 'price']
    # Tìm kiếm theo name
    column_searchable_list = ['name']
    # Fileter lọc theo price và name
    column_filters = ['price', 'name']
    # Chỉnh sủa tên trực tiếp trên web
    column_editable_list = ['name']
    # Xuất ra file .csv
    can_export = True

    # Chứng thực, đăng nhập thì mới hiện trang product
    # def is_accessible(self):
    #     return current_user.is_authenticated

# Tab Category
class MyCategoryView(AuthenticatedAdmin):
    column_list =['name', 'products']









# Tab thống kê báo cáo
class MyStatsView(AuthenticatedManager):
    @expose("/")
    def index(self):
        return self.render('admin/stats.html')


# Tab đăng xuất
class MyLogoutView(AuthenticatedUser):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')

# Tạo trang admin có tên là Home-QUẢN TRỊ BÁN HÀNG (Dùng bootstrap4: thư viện hỗ trợ sẵn)
admin = Admin(app=app, name="QUẢN TRỊ BÁN HÀNG", template_mode='bootstrap4')
admin.add_view(MyCategoryView(Category, db.session))
admin.add_view(MyProductView(Product, db.session))
admin.add_view(MyStatsView(name='Thông kê báo cáo'))
admin.add_view(MyLogoutView(name='Đăng xuất'))
