from django.db import models
from django.contrib.auth.models import AbstractUser





class User(AbstractUser):
    patronymic = models.CharField(max_length=255, blank=True, null=True, verbose_name="Отчество")
    date_birth = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    
    

    class Meta: # класс можно менять и после миграции, имена будут изменены, в полях verbose_name тоже
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
    
    
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import Group

@receiver(m2m_changed, sender=User.groups.through) #декоратор,  который  регистрирует  функцию  `update_user_is_staff`  как  обработчик  сигнала
# изменяется  отношение  "многие-ко-многим" отношение User к Group
def update_user_is_staff(sender, instance, action, reverse, model, pk_set, **kwargs): 
    if action == 'post_add' and 'Сотрудник' in [Group.objects.get(pk=pk).name for pk in pk_set]: # Проверка,  была  ли  выполнена  операция  добавления  пользователя  в  группу.
        instance.is_staff = True
        instance.save()