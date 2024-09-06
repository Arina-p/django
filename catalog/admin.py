from django.contrib import admin

from catalog.models import Category, Product

#admin.site.register(Category)
#admin.site.register(Product)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin): # в этом классе можем описать многие способы по настройке отображения в админ-панели
    prepopulated_fields = {'slug': ('name',)} # поля которые нужно заполнять автоматически, здесь для автоматического слага


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin): # в этом классе можем описать многие способы по настройке отображения в админ-панели
    #prepopulated_fields = {'slug': ('name',)} 
    list_display = ['name', 'quantity', 'price'] # отображаются все эти поля, а не только название
    list_editable = ['quantity', 'price'] # редактировать поле, не открывая каждую запись
    search_fields = ['name', 'description'] # поиск по полям
    list_filter = ['quantity', 'category'] # фильтрация

    # fields в каком порядке будут поля, можно в одну строку, какие вообще будут отображаться
    # fields = [ 
    #     "name",
    #        ...
    #     ("price", "quantity"),
    # ]