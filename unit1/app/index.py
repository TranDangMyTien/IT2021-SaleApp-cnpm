# Phần Controller trong mô hình
import math
from flask import render_template, request, redirect, session, jsonify
# Đối tượng session nằm trên server lưu tạm giỏi hàng (không cần lưu trong database)
import dao,utils
# dao: truy vấn databasse, utils thực hiện các chức năng tiện ích
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
    flight_id = request.args.get('flight_id')
    page = request.args.get("page")

    flights = dao.load_flights() #Gọi hàm bên modul khác
    flighttickets = dao.load_flighttickets(kw=kw, flight_id=flight_id, page=page)
    # Số lượng sản phẩm trong data
    total = dao.count_flightticket()

    # Gửi thông tin ra ngoài (gửi lên web)
    return render_template('index.html', flights=flights,
                           flighttickets=flighttickets,
                           pages=math.ceil(total / app.config['PAGE_SIZE']))
    #categories là tên biến, cates là giá trị gửi ra
    # math.ceil là hàm làm tròn lên : 1,2 -> 2


# Trang chi tiết sản phẩm
@app.route('/flighttickets/<id>')
def details(id):
    # Trả về dạng html
    comments = dao.get_comments_by_prod_id(id)
    return render_template('details.html', flightticket=dao.get_flightticket_by_id(id), comments=comments)

# Thêm bình luận
@app.route("/api/flighttickets/<id>/comments", methods=['post'])
@login_required
def add_comment(id):
    content = request.json.get('content')

    try:
        c = dao.add_comment(flightticket_id=id, content=content)
    except:
        return jsonify({'status': 500, 'err_msg': 'Hệ thống đang có lỗi!'})
    else:

        return jsonify({'status': 200, "c": {'content': c.content, "user": {"avatar": c.user.avatar}}})


# Trang đăng nhập
# get : truy cập vào trang
# post : để submit
@app.route("/login", methods=['get', 'post'])
def login_user_process():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)
        # args : lấy tham số trên URL (lấy 'next')
        next = request.args.get('next')
        # Nếu như trên URL không có 'next' thì trả vè '/' (trang chủ)
        return redirect("/" if next is None else next)
    return render_template('login.html')

# Trang đăng xuất
@app.route('/logout')
def process_logout_user():
    logout_user()
    # Đăng xuất xong thì về trang đăng nhập
    return redirect("/login")


# Trang đăng ký
@app.route('/register', methods=['get', 'post'])
def register_user():
    err_msg = ""
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password.__eq__(confirm):
            try:
                # Tập tin gửi lên đều nằm trong request.files
                dao.add_user(name=request.form.get('name'),
                             username=request.form.get('username'),
                             password=password,
                             avatar=request.files.get('avatar'))
            except:
                err_msg = 'Hệ thống đang bị lỗi!'
            else:
                return redirect('/login')
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('register.html', err_msg=err_msg)



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


# Phần giỏ hàng
# Bắt đầu bằng api là gọi bằng jsonify
@app.route('/api/cart', methods=['post'])
def add_cart():
    """
    {
    "cart": {
            "1": {
                "id": 1,
                "name": "ABC",
                "price": 12,
                "quantity": 2
            }, "2": {
                "id": 2,
                "name": "ABC",
                "price": 12,
                "quantity": 2
            }
        }
    }
    :return:
    """
    # Biến 'cart' là mình tự đặt
    cart = session.get('cart')
    if cart is None:
        cart = {}

    data = request.json
    id = str(data.get("id"))

    if id in cart: # san pham da co trong gio
        cart[id]["quantity"] = cart[id]["quantity"] + 1
    else: # san pham chua co trong gio
        cart[id] = {
            "id": id,
            "name": data.get("name"),
            "price": data.get("price"),
            # Thêm biến quantity (số lượng)
            "quantity": 1
        }
    # Cập nhật lại giỏ hàng
    session['cart'] = cart
    return jsonify(utils.count_cart(cart))

# Cập nhật số lượng
# api đánh dấu hàm gọi bằng js
# methods = put : để cập nhật
@app.route("/api/cart/<flightticket_id>", methods=['put'])
def update_cart(flightticket_id):
    cart = session.get('cart')
    # Kiểm tra có giỏ hàng chưa và kiểm tra sản phẩm có trong giỏi chưa
    if cart and flightticket_id in cart:
        # Lấy số lượng ra (số lượng mua sản phẩm)
        quantity = request.json.get('quantity')
        # Khi nó gửi lên là chuỗi thì bây giờ xử lý phải đưa về số
        cart[flightticket_id]['quantity'] = int(quantity)

    # Cập nhật lại giỏ hàng
    session['cart'] = cart
    return jsonify(utils.count_cart(cart))


# Xóa sản phẩm
@app.route("/api/cart/<flightticket_id>", methods=['delete'])
def delete_cart(flightticket_id):
    cart = session.get('cart')
    if cart and flightticket_id in cart:
        del cart[flightticket_id]

    # Cập nhật lại giỏi hàng
    session['cart'] = cart
    return jsonify(utils.count_cart(cart))

# Hàm thanh toán
@app.route('/api/pay', methods=['post'])
def pay():
    try:
        dao.add_receipt(session.get('cart'))
    except:
        return jsonify({'status': 500, 'err_msg': 'Hệ thống đang có lỗi!'})
    else:
        del session['cart']
        return jsonify({'status': 200})




# Trang giỏi hàng
@app.route('/cart')
# Danh sách các phần tử trong giỏi
def cart_list():
    return render_template('cart.html')


# Hàm trả chung (trên thanh menu đều có dù ở / (trang nào))
@app.context_processor
def common_resp():
    return {
        'flights': dao.load_flights(),
        # Đưa thông tin giỏi hàng từ bàn đầu, không cần click thêm mới hiện
        'cart': utils.count_cart(session.get('cart'))
    }


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)




#Điều kiện này kiểm tra xem script có đang được chạy trực tiếp hay không (không phải là được import như một module).
#Nếu đúng, phương thức app.run() được gọi, nó khởi động máy chủ phát triển Flask, cho phép ứng dụng có thể được truy cập từ client.
if __name__ == '__main__':
    from app import admin
    app.run(debug=True) #Có báo lỗi sẽ xuất ra










# render_template được sử dụng để hiển thị nội dung trang web,
# trong khi redirect được sử dụng để chuyển hướng người dùng sang một đường dẫn khác.



















