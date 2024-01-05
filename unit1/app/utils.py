# Phần hỗ trợ
# Đếm sản phẩm trong giỏi hàng
def count_cart(cart):
    total_quantity, total_amount = 0, 0

    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_amount += c['quantity']*c['price']

    return {
        # Tổng số sản phẩm
        "total_quantity": total_quantity,
        # Tổng giá tiền
        "total_amount": total_amount
    }