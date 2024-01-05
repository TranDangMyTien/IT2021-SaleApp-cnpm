//PHẦN GIỎ HÀNG (trên server)
//Hàm thêm sản phẩm
function addToCart(id, name, price) {
    fetch('/api/cart', {
        method: "post",
//        Ép lên thành chuỗi
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        headers: {
            'Content-Type': "application/json"
        }
    }).then(function(res) {
//   Hàm then(function(res) là phản hồi từ server, chạy bất đồng bộ
        return res.json();
//   Dữ liệu từ hàm trước sau khi chạy xong sẽ quăng vào biến hàm sau. Quăng vào biến data phía dưới
    }).then(function(data) {
        let c = document.getElementsByClassName('cart-counter');
        for (let d of c)
//      Hiển thị tổng số lượng sản phẩm
            d.innerText = data.total_quantity
    })
}



// Hàm cập nhật
//obj là tham số this bên 'cart.html'
function updateCart(id, obj) {
    obj.disabled = true;
    fetch(`/api/cart/${id}`, {
        method: 'put',
        body: JSON.stringify({
            'quantity': obj.value
        }),  headers: {
            'Content-Type': "application/json"
        }
    }).then(res => res.json()).then(data => {
        obj.disabled = false;
        let c = document.getElementsByClassName('cart-counter');
        for (let d of c)
            d.innerText = data.total_quantity
    });
}