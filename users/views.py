from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from users.forms import LoginUserForm, RegisterUserForm

from orders.models import Order, OrderItem
from direction.models import Membership, Record
from django.db.models import Prefetch
from datetime import date, datetime
from functools import wraps
from django.http import HttpResponseForbidden

from django.db.models import Prefetch, Case, When, BooleanField, Value


def group_required(group_name):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("У вас нет доступа к этой странице.")
        return wrapper
    return decorator

class LoginUser(LoginView):
    form_class = LoginUserForm # или 1 вариант был использовать  AuthenticationForm
    # если AuthenticationForm то Имя пользователя Пароль, если наш - то, что указали - Логин Пароль
    template_name = 'users/login.html'
    
    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name='Владелец ИС').exists():
            self.success_url = 'main:home'
        elif user.groups.filter(name='Сотрудник').exists():
            self.success_url = 'main:home'
        else:
            self.success_url = 'users:profile'
        return reverse_lazy(self.success_url) # 'main:home'
    # или LOGIN_REDIRECT_URL вместо ф-ии

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    def form_valid(self, form):
        response = super().form_valid(form)
        group = Group.objects.get(name='Клиент') # Замените на имя вашей группы
        self.object.groups.add(group)
        
        return response

@login_required
def profiledetail(request):
    user = request.user
    excluded_fields = ['password'] # Список исключенных полей
    profile_data = {
    'Логин': user.username,
    'Фамилия': user.last_name,
    'Имя': user.first_name,
    'Отчество': user.patronymic,
    'Email': user.email,
    'Дата рождения': user.date_birth,
    'Телефон': user.phone,
    'Дата регистрации': user.date_joined,
    }

    # prefetch_related в обратном порядке FK от OrderItem к Order (а в корзине напр от корзины к продуктам в корзине)
    orders = Order.objects.filter(user=request.user).prefetch_related( 
                Prefetch(
                    "orderitem_set",
                    queryset=OrderItem.objects.select_related("product"),
                )
            ).order_by("-id")
    # Загрузка абонементов пользователя
    active_memberships = Membership.objects.filter(user=user).annotate(
        is_active=Case(
            When(start_date__lte=date.today(), end_date__gte=date.today(), then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        )
    ).filter(is_active=True)
    # Получение активных записей пользователя
    active_records = Record.objects.filter(
        membership__user=user, # Фильтруем по пользователю через абонемент
        fitnessclass__class_date__gt=datetime.now()  # Фильтруем по занятиям, которые еще не прошли
    ).select_related('membership', 'fitnessclass')
    # Получение неактивных записей пользователя
    inactive_records = Record.objects.filter(
        membership__user=user,
        fitnessclass__class_date__lte=datetime.now() 
    ).select_related('membership', 'fitnessclass')

    context = {
    'profile_data': profile_data,
    'orders': orders,
    'active_memberships': active_memberships,
    'active_records': active_records,
    'inactive_records': inactive_records,
    }
    return render(request, 'users/profile.html', context)



def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))

def users_cart(request):
    return render(request, 'users/users_cart.html')
