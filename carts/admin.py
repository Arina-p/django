from django.contrib import admin

# Register your models here.
from carts.models import Cart



class CartTabAdmin(admin.TabularInline):
    model = Cart
    fields = "product", "created_timestamp"
    search_fields = "product", "created_timestamp"
    readonly_fields = ("created_timestamp",)
    extra = 1

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin): # в этом классе можем описать многие способы по настройке отображения в админ-панели
    list_display = ['user', 'product'] # отображаются все эти поля, а не только название
    