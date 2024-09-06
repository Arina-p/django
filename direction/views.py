from django.shortcuts import render, redirect
from django.db.models.functions import ExtractWeekDay
# Create your views here.
from .models import Direction, FitnessClass, Instructor, Record
from django.db.models import IntegerField, Value
import calendar
from datetime import datetime
from django.core.exceptions import ValidationError
from django.contrib import messages

def show_directions(request):
    directions = Direction.objects.all()  # Получаем все направления из БД
    return render(request, 'direction/direction.html', {'directions': directions})

def schedule_view(request): 
    current_month = int(request.GET.get('month', datetime.now().month))  # Получаем месяц из запроса или по умолчанию текущий
    classes = FitnessClass.objects.filter(class_date__month=current_month)  # Фильтруем по месяцу
    weekdays = list(calendar.day_name)  # Получаем названия дней недели
    russian_month_names = {
        1: "Январь",
        2: "Февраль",
        3: "Март",
        4: "Апрель",
        5: "Май",
        6: "Июнь",
        7: "Июль",
        8: "Август",
        9: "Сентябрь",
        10: "Октябрь",
        11: "Ноябрь",
        12: "Декабрь"
    }
    russian_weekday_names = [
       "Понедельник", 
       "Вторник",
       "Среда",
       "Четверг",
       "Пятница",
       "Суббота",
       "Воскресенье"
   ]
    schedule = {}  

    for cls in classes:
        week_number = cls.class_date.isocalendar().week  
        weekday = calendar.day_name[cls.class_date.weekday()]

        if week_number not in schedule:
            schedule[week_number] = {}  

        if weekday not in schedule[week_number]:
            schedule[week_number][weekday] = []  

        schedule[week_number][weekday].append(cls)
    
    user_memberships = None
    if request.user.is_authenticated:
        
        all_memberships = request.user.membership_set.all()
        user_memberships = filter(lambda m: m.status(), all_memberships)

    return render(request, 'direction/schedule.html', {
        'schedule': schedule,
        'current_month': current_month,
        'weekdays': russian_weekday_names,
        'russian_month_names': russian_month_names,
        'russian_weekday_names': russian_weekday_names,
        'user_memberships': user_memberships
    })

def signup_for_class(request, class_id):
    if request.method == 'POST' and request.user.is_authenticated:
        membership_id = request.POST.get('membership_id')
        # 1. Проверка на существующую запись
        existing_signup = Record.objects.filter(
            membership_id=membership_id, fitnessclass_id=class_id
        ).exists()
        if existing_signup:
            messages.error(request, 'Вы уже зарегистрированы на это занятие.')
        else:
            try:
                # Создаем экземпляр Record и вызываем его метод save(), который обрабатывает валидацию
                record = Record(membership_id=membership_id, fitnessclass_id=class_id)
                record.save()
                messages.success(request, 'Вы успешно записались на занятие!')
                # Перенаправляем на страницу успеха или обратно на расписание
                return redirect('schedule')  # Или любой другой подходящий URL
            except ValidationError as e:
                # Обрабатываем ошибки валидации (отображаем их пользователю)
                messages.error(request, str(e))

    if not request.user.is_authenticated:
        messages.info(request, 'Для записи на занятия необходимо авторизоваться.')
    
    return redirect('schedule')    


def show_instructors(request):
    instructors = Instructor.objects.all()
    return render(request, 'direction/instructors.html', {'instructors': instructors})