from django.urls import path
from . import views # or from catalog

app_name = 'cart' 

urlpatterns = [
    path('cart_add/', views.cart_add, name='cart_add'),
    path('cart_remove/', views.cart_remove, name='cart_remove'),
]