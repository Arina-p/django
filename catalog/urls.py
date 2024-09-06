from django.urls import path
from . import views

app_name = 'catalog'
urlpatterns = [
    path('<slug:category_slug>/', views.catalog, name='catalog'),
]
