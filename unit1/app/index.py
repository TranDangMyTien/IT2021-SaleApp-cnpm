# Phần Controller trong mô hình
import math
from flask import render_template, request, redirect, session, jsonify
import dao
from app import app, login
from flask_login import login_user, logout_user, login_required



#Dòng này là một decorator (bộ trang trí), nó gắn liên kết với hàm bên dưới với URL gốc ("/") của ứng dụng web.
#Nghĩa là khi người dùng truy cập vào URL gốc của ứng dụng, hàm bên dưới sẽ được thực thi.
@app.route('/') #Định tuyến đường dẫn. Mặc định nhận get
def index():
    #Những thông tin từ client gửi lên server đều được đóng gói trong request (c->v: Mô dình mcv)
    #Lấy giá trị của tham số được truyền trong URL
    #Qua phần layout/header để xem cách lấy trong URL
    kw = request.args.get('kw')
    cate_id = request.args.get('cate_id')
    page = request.args.get("page")

    cates = dao.load_categories() #Gọi hàm bên modul khác
    products = dao.load_products(kw=kw, cate_id=cate_id, page=page)
    # Số lượng sản phẩm trong data
    total = dao.count_product()

    # Gửi thông tin ra ngoài (gửi lên web)
    return render_template('index.html',categories = cates,
                           products=products,
                           pages=math.ceil(total / app.config['PAGE_SIZE']))
    #categories là tên biến, cates là giá trị gửi ra
    # math.ceil là hàm làm tròn lên : 1,2 -> 2




@app.route('/admin/login', methods=['post'])
def login_admin_process():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)
    # redirect: chuyển trang
    # Sau khi đăng nhập thì chuyển về trang admin
    return redirect('/admin')


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)




#Điều kiện này kiểm tra xem script có đang được chạy trực tiếp hay không (không phải là được import như một module).
#Nếu đúng, phương thức app.run() được gọi, nó khởi động máy chủ phát triển Flask, cho phép ứng dụng có thể được truy cập từ client.
if __name__ == '__main__':
    from app import admin
    app.run(debug=True) #Có báo lỗi sẽ xuất ra