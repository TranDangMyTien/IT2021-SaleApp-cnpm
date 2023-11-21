def load_categories():
    return [
        {
            'id':1,
            'name':'Mobile'
        },
        {
            'id': 2,
            'name': 'Tablet'
        }
    ]

# Hàm liệt kê các sản phẩm
def load_products(kw=None):
    products = [
        {
            "id": 1,
            "name": "Iphone 15 Pro Max",
            "price": 20000000,
            "image": "https://images.fpt.shop/unsafe/fit-in/960x640/filters:quality(90):fill(white):upscale()/fptshop.com.vn/Uploads/Originals/2023/9/13/638302015849272512_iPhone_15_Pink_Pure_Back_iPhone_15_Pink_Pure_Front_2up_Screen__USEN.jpg"
        },
        {
            "id": 2,
            "name": "Iphone 15",
            "price": 20000000,
            "image": "https://images.fpt.shop/unsafe/fit-in/960x640/filters:quality(90):fill(white):upscale()/fptshop.com.vn/Uploads/Originals/2023/9/13/638302015849272512_iPhone_15_Pink_Pure_Back_iPhone_15_Pink_Pure_Front_2up_Screen__USEN.jpg"
        },
        {
            "id": 3,
            "name": "Ipad Pro 2022",
            "price": 20000000,
            "image": "https://images.fpt.shop/unsafe/fit-in/960x640/filters:quality(90):fill(white):upscale()/fptshop.com.vn/Uploads/Originals/2023/9/13/638302015849272512_iPhone_15_Pink_Pure_Back_iPhone_15_Pink_Pure_Front_2up_Screen__USEN.jpg"
        },
        {
            "id": 4,
            "name": "Iphone 15",
            "price": 20000000,
            "image": "https://images.fpt.shop/unsafe/fit-in/960x640/filters:quality(90):fill(white):upscale()/fptshop.com.vn/Uploads/Originals/2023/9/13/638302015849272512_iPhone_15_Pink_Pure_Back_iPhone_15_Pink_Pure_Front_2up_Screen__USEN.jpg"
        },
        {
            "id": 5,
            "name": "Iphone 15",
            "price": 20000000,
            "image": "https://images.fpt.shop/unsafe/fit-in/960x640/filters:quality(90):fill(white):upscale()/fptshop.com.vn/Uploads/Originals/2023/9/13/638302015849272512_iPhone_15_Pink_Pure_Back_iPhone_15_Pink_Pure_Front_2up_Screen__USEN.jpg"
        }
    ]
    if kw: # Bằng nghĩa với cú pháp if kw is not None
        products = [p for p in products if p['name'].find(kw) >= 0]
    return products


