from django.urls import path
from .views import ProductView,CartView,QuantityView,CreateOrderView

urlpatterns=[
    path('product/',ProductView.as_view()),
    path('cart/',CartView.as_view()),
    path('updatequantity/',QuantityView.as_view()),
    path('createorder/',CreateOrderView.as_view())
]