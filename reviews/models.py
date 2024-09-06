from django.db import models
from django.urls import reverse
from users.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Review(models.Model): 
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.IntegerField(verbose_name = 'Оценка')
    
    review_text = models.TextField(verbose_name = 'Текст отзыва')
    review_date = models.DateField(verbose_name = 'Дата добавления отзыва')
    
    
    class Meta: 
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        db_table = 'reviews'

    def __str__(self):
        return self.review_text
