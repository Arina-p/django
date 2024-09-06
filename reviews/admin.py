from django.contrib import admin

# Register your models here.

from reviews.models import Review

@admin.register(Review)
# CartAdmin
class ReviewAdmin(admin.ModelAdmin): # в этом классе можем описать многие способы по настройке отображения в админ-панели
    list_display = ['user', 'rating', 'review_text'] # отображаются все эти поля, а не только название