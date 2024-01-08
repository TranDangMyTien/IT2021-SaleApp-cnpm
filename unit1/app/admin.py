from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose, AdminIndexView
from app import app, db, dao
from app.models import Flight, FlightTicket
from flask_login import logout_user, current_user
from flask import redirect, request
from app.models import UserRoleEnum


class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', stats=dao.count_flighttickets_by_flight())


# Tạo lớp chứng thực tài khoản thì mới thấy tab nào đó
class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


# Tạo lớp chứng thực cho kiểu Model, và nó là role Admin
class AuthenticatedEmployee(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.EMPLOYEE


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN


# Lớp chứng thực cho nhân viên và quản trị

class AuthenticatedAdminAndEmployee(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and (
                    current_user.user_role == UserRoleEnum.ADMIN or current_user.user_role == UserRoleEnum.EMPLOYEE)


# MyFlightTicketView kế thừa lại ModelView
class MyFlightTicketView(AuthenticatedAdminAndEmployee):
    # Tab FlightTicket (trong trang admin) : chỉ hiện những cột dưới
    column_list = ['id', 'name', 'price']
    # Tìm kiếm theo name
    column_searchable_list = ['name']
    # Fileter lọc theo price và name
    column_filters = ['price', 'name']
    # Chỉnh sủa tên trực tiếp trên web
    column_editable_list = ['name']
    # Xuất ra file .csv
    can_export = True

    # Chứng thực, đăng nhập thì mới hiện trang FlightTicket
    # def is_accessible(self):
    #     return current_user.is_authenticated


# Tab Flight
class MyFlightView(AuthenticatedAdminAndEmployee):
    column_list = ['name', 'flighttickets']


# Tab thống kê báo cáo
class MyStatsView(AuthenticatedUser):
    @expose("/")
    def index(self):
        kw = request.args.get("kw")
        return self.render('admin/stats.html',
                           stats=dao.revenue_stats(kw),
                           month_stats=dao.revenue_stats_by_month())


# Tab đăng xuất
class MyLogoutView(AuthenticatedUser):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')


# Tạo trang admin có tên là Home-QUẢN TRỊ BÁN HÀNG (Dùng bootstrap4: thư viện hỗ trợ sẵn)
admin = Admin(app=app, name="QUẢN TRỊ BÁN HÀNG", template_mode='bootstrap4', index_view=MyAdminIndex())

admin.add_view(MyFlightView(Flight, db.session))

admin.add_view(MyFlightTicketView(FlightTicket, db.session))

admin.add_view(MyStatsView(name='Thông kê báo cáo'))

admin.add_view(MyLogoutView(name='Đăng xuất'))
