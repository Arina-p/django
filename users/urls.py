from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'), # users:login
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('profile/', views.profiledetail, name='profile'),
    path('users-cart/', views.users_cart, name='users_cart'),
   
]