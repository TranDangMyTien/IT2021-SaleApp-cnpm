from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose
from app import app, db
from app.models import Category, Product

# MyProductView kế thừa lại ModelView
class MyProductView(ModelView):
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


class MyCategoryView(ModelView):
    column_list =['name', 'products']

class StatsView(BaseView):
    @expose("/")
    def index(self):
        return self.render('admin/stats.html')


admin = Admin(app=app, name="QUẢN TRỊ BÁN HÀNG", template_mode='bootstrap4')
admin.add_view(MyCategoryView(Category, db.session))
admin.add_view(MyProductView(Product, db.session))
admin.add_view(StatsView(name='Thông kê báo cáo'))
