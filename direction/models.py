from django.db import models
# from users.models import User
from datetime import datetime
from django.utils import timezone

from django.forms import ValidationError

from orders.models import OrderItem, Order
from catalog.models import Product
from datetime import  date
from datetime import timedelta
from users.models import User

from django.db.models.signals import pre_save
from django.dispatch import receiver

from django.db.models.signals import post_save


# Create your models here.
class Direction(models.Model):
    name = models.CharField(max_length = 150, unique = True, verbose_name = 'Название') # unique = True значение должно быть уникальным
    slug = models.SlugField(max_length = 200, unique = True, blank = True, null = True, verbose_name = 'URL')
    description = models.TextField(blank = True, null = True, verbose_name = 'Описание')
    image = models.ImageField(upload_to='direction_images', blank = True, null = True, verbose_name = 'Изображение') # хранится не само изобр, а путь к нему
    duration = models.CharField(max_length = 50, verbose_name = 'Длительность')

    class Meta: # класс можно менять и после миграции, имена будут изменены, в полях verbose_name тоже
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'
        db_table = 'direction'
        ordering = ('id', ) # сортировка, порядок

    def __str__(self):
        return self.name
    
class Instructor(models.Model):
    last_name = models.CharField(max_length = 150, verbose_name = 'Фамилия')
    name = models.CharField(max_length = 150, verbose_name = 'Имя')
    middle_name = models.CharField(max_length = 150, blank = True, null = True, verbose_name = 'Отчество')
    about = models.TextField(blank = True, null = True, verbose_name = 'Описание')
    image = models.ImageField(upload_to='instructors_images', blank = True, null = True, verbose_name = 'Изображение') # хранится не само изобр, а путь к нему
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")

    class Meta: # класс можно менять и после миграции, имена будут изменены, в полях verbose_name тоже
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренеры'
        db_table = 'instructor'
        ordering = ('id', ) # сортировка, порядок

    def __str__(self):
        return f'{self.last_name} {self.name}'
    
class FitnessClass(models.Model):
    direction = models.ForeignKey(to=Direction, on_delete=models.CASCADE, verbose_name='Направление')
    class_date = models.DateTimeField(verbose_name = 'Дата и время занятия')
    instructor = models.ForeignKey(to=Instructor, on_delete=models.SET_NULL, blank = True, null = True, verbose_name = 'Инструктор')
    # instructor = models.CharField(max_length = 150, blank = True, null = True, verbose_name = 'Инструктор')
    place = models.CharField(max_length = 150, verbose_name = 'Место проведения занятия')
    number = models.PositiveIntegerField(default = 0, verbose_name = 'Количество свободных мест на занятие')
    
    def get_weekday(self):
        weekday = datetime.strftime(self.class_date, '%A')  # Получаем день недели (напр., 'Monday')
        return weekday
    
    class Meta: 
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'
        db_table = 'schedule'
        ordering = ('class_date', )
    
    def __str__(self):
        date = self.class_date.strftime('%A')
        return f'Занятие {self.direction.name} | Время проведения {self.class_date} {date}'


class Membership(models.Model):
    order_item = models.ForeignKey(to=OrderItem, on_delete=models.SET_DEFAULT, null=True, verbose_name="Заказ", default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Тип абонемента")
    start_date = models.DateField(verbose_name="Дата начала действия")
    end_date = models.DateField(verbose_name="Дата окончания действия", default=None)

    number = models.PositiveIntegerField(verbose_name="Количество доступных занятий", default=None)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="Клиент", default=None)
    
    def save(self, *args, **kwargs):
        if not self.pk:  # If the instance is being created (no primary key yet)
            self.number = self.product.quantity  # Set quantity from the product
            self.calculate_end_date() # self
        super().save(*args, **kwargs)  # Call the parent save() method
    
    def calculate_end_date(self):
        validity_period = self.product.validity_period
        self.end_date = self.start_date + timedelta(days=validity_period)
        # self.save()

    def status(self):
        today = date.today()
        return self.start_date <= today <= self.end_date
        
    
#f'Membership {self.pk} for {self.user}'
    class Meta: 
        verbose_name = 'Абонемент'
        verbose_name_plural = 'Абонементы'
        db_table = 'membership'
    def __str__(self):
        return f'Абонемент {self.user} {self.product} id{self.pk}'

@receiver(pre_save, sender=Membership)
def update_membership_fields(sender, instance, **kwargs):
    if not instance.pk:  # If the instance is being created
        instance.user = instance.order_item.order.user
        instance.product = instance.order_item.product
        instance.number = instance.product.quantity
        instance.calculate_end_date() 


class Record(models.Model):
    membership = models.ForeignKey(to=Membership, on_delete=models.CASCADE, verbose_name="Абонемент")
    fitnessclass = models.ForeignKey(to=FitnessClass, on_delete=models.CASCADE, verbose_name="Занятие")

    def clean(self):
        # Проверка статуса абонемента
        if not self.membership.status():
            raise ValidationError("Абонемент не действителен.")
        # Проверка количества доступных занятий
        if self.membership.number < 1:
            raise ValidationError("Количество доступных занятий в абонементе исчерпано.")
        # Проверка количества доступных мест на занятие
        if self.fitnessclass.number < 1:
            raise ValidationError("Нет свободных мест на это занятие.")
        # Проверка времени до занятия (2 часа)
        time_until_class = self.fitnessclass.class_date - timezone.now()
        if time_until_class.total_seconds() < 7200:
            raise ValidationError("Запись на занятие возможна не менее чем за 2 часа до начала.")
    def save(self, *args, **kwargs):
        self.full_clean()  # Выполняем валидацию перед сохранением
        super().save(*args, **kwargs) 

        # Уменьшаем количество доступных занятий в абонементе 
        self.membership.number -= 1
        self.membership.save()

        # Уменьшаем количество доступных мест на занятии
        self.fitnessclass.number -= 1
        self.fitnessclass.save()

    class Meta: 
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        db_table = 'record'
    def __str__(self):
        return f'Запись {self.membership.user} на занятие {self.fitnessclass.direction} {self.fitnessclass.class_date}'
    

@receiver(post_save, sender=Order)
def create_memberships_on_order_paid(sender, instance, created, **kwargs):
    if instance.status == 'Оплачен':  # Проверяем, оплачен ли заказ
        order_items = instance.orderitem_set.all()  # Получаем элементы заказа
        for item in order_items:
            # Проверяем, является ли продукт абонементомif item.product.is_membership:  
            Membership.objects.create(
                order_item=item,
                product=item.product,
                user=instance.user,
                start_date=item.membership_start_date  # Используем дату начала действия из OrderItem
            )