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

//Hàm xóa và xử lý xác nhận xóa
function deleteCart(id, obj) {
    if (confirm("Bạn có chắc chắn xóa không?") === true) {
        obj.disabled = true;
        fetch(`/api/cart/${id}`, {
            method: 'delete'
        }).then(res => res.json()).then(data => {
            obj.disabled = false;
            let c = document.getElementsByClassName('cart-counter');
            for (let d of c)
                d.innerText = data.total_quantity

            let r = document.getElementById(`product${id}`);
//            Ẩn đi những cái đã xóa trong trang giỏi hàng
            r.style.display = "none";
        });
    }
}


//Hàm thanh toán, xác nhận người dùng có muốn thanh toán
function pay() {
    if (confirm("Bạn chắc chắn thanh toán!") === true) {
        fetch("/api/pay", {
            method: "post"
        }).then(res => res.json()).then(data => {
//        == 200 là thành công
            if (data.status === 200)
                location.reload();
            else
                alert(data.err_msg);
        })
    }
}