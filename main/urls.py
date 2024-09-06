from django.urls import path
from main.views import index
from reviews.views import add_review

app_name = 'main'
urlpatterns = [
    path('', index, name='home'),
    path('add_review/', add_review, name='add_rev')
]