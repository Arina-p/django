from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length = 150, unique = True, verbose_name = 'Название') 
    slug = models.SlugField(max_length = 200, unique = True, blank = True, null = True, verbose_name = 'URL')   
    class Meta: 
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
        db_table = 'category'
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length = 150, unique = True, verbose_name = 'Название') 
    description = models.TextField(blank = True, null = True, verbose_name = 'Описание')
    validity_period = models.PositiveIntegerField(default = 0, verbose_name = 'Срок действия')
    price = models.PositiveIntegerField(default = 0, verbose_name = 'Стоимость')
    quantity = models.PositiveIntegerField(default = 0, verbose_name = 'Количество доступных занятий')
    category = models.ForeignKey(to=Category, on_delete= models.CASCADE, verbose_name = 'Категория')  
    def __str__(self):
        return f'{self.name}' 
    def display_id(self):
        return f'{self.id:05}'
    def sell_price(self):
        return self.price
    class Meta: 
        verbose_name = 'Тип абонемента'
        verbose_name_plural = 'Типы абонементов'
        db_table = 'product'
        ordering = ('id', ) 
    def get_absolute_url(self):
        return reverse("catalog:product", kwargs={"product_slug": self.slug})
    

