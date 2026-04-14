from django.urls import path
from .views import home, product_detail, update_price

urlpatterns = [
    path('', home, name='home'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('update-price/<slug:slug>/', update_price, name='update_price'),
]
