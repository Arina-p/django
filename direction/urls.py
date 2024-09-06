from django.urls import path
from . import views # or from catalog


urlpatterns = [
    path('', views.show_directions, name='directions'),
    path('schedule/', views.schedule_view, name='schedule'),
    path('instructors/', views.show_instructors, name='instructors'),
    path('signup/<int:class_id>/', views.signup_for_class, name='signup_for_class'),
]