from django.urls import path
from .views import (home,
                    product_detail,
                    update_price,
                    cart_detail,
                    cart_add,
                    checkout,
                    contact,
                    blog_list,
                    blog_detail,
                    cart_remove)

urlpatterns = [
    path('', home, name='home'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('update-price/<slug:slug>/', update_price, name='update_price'),
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('checkout/', checkout, name='checkout'),
    path('contact/', contact, name='contact'),
    path('blog/', blog_list, name='blog_list'),
    path('blog/<slug:slug>/', blog_detail, name='blog_detail'),
]
