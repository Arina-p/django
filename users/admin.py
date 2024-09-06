from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from carts.models import Cart
from carts.admin import CartTabAdmin

#admin.site.register(User, UserAdmin)


UserAdmin.fieldsets += ('Custom fields set', {'fields': ('patronymic', 'date_birth', 'phone')}),



@admin.register(User) 
class UserAdmin(admin.ModelAdmin): # в этом классе можем описать многие способы по настройке отображения в админ-панели
    #prepopulated_fields = {'slug': ('name',)} 
    list_display = ['username', 'first_name', 'last_name'] # отображаются все эти поля, а не только название
    #list_editable = ['username', 'first_name', 'last_name'] # редактировать поле, не открывая каждую запись
    search_fields = ['username', 'first_name', 'last_name'] # поиск по полям

    inlines = [CartTabAdmin,]


    