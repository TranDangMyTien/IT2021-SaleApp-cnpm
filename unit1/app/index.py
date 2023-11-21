# Phần Controller trong mô hình
from flask import Flask, render_template, request #Dòng này import module Flask, cần thiết để tạo ứng dụng web.
import dao
#Dòng này tạo một instance của class Flask và gán cho biến app.
#Biến __name__ là một biến đặc biệt trong Python và đại diện cho tên của module hiện tại.
app = Flask(__name__)

#Dòng này là một decorator (bộ trang trí), nó gắn liên kết với hàm bên dưới với URL gốc ("/") của ứng dụng web.
#Nghĩa là khi người dùng truy cập vào URL gốc của ứng dụng, hàm bên dưới sẽ được thực thi.
@app.route('/') #Định tuyến đường dẫn. Mặc định nhận get
def index():
    #Những thông tin từ client gửi lên server đều được đóng gói trong request (c->v: Mô dình mcv)
    kw = request.args.get('kw')
    cates = dao.load_categories() #Gọi hàm bên modul khác
    products = dao.load_products(kw=kw)
    return render_template('index.html', categories = cates, products = products)
    #categories là tên biến, cates là giá trị gửi ra


@app.route('/products/<id>')
def details(id):
    return render_template('details.html')

#Điều kiện này kiểm tra xem script có đang được chạy trực tiếp hay không (không phải là được import như một module).
#Nếu đúng, phương thức app.run() được gọi, nó khởi động máy chủ phát triển Flask, cho phép ứng dụng có thể được truy cập từ client.
if __name__ == '__main__':
    app.run(debug=True) #Có báo lỗi sẽ xuất ra