from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from direction.models import Direction, FitnessClass, Instructor, Membership, Record

@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin): # в этом классе можем описать многие способы по настройке отображения в админ-панели
    list_display = ['name', 'duration'] # отображаются все эти поля, а не только название
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(FitnessClass)

admin.site.register(Instructor)

#admin.site.register(Membership)

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    # ... existing code ...
    readonly_fields = ('product','number', 'end_date', 'user')  # Make fields read-only

    def save_model(self, request, obj, form, change):
        if not change:  # Only for newly created instances
            obj.user = obj.order_item.order.user
            obj.product = obj.order_item.product
            obj.number = obj.product.quantity
            obj.calculate_end_date()  # Calculate and set end date
        super().save_model(request, obj, form, change)

# admin.site.register(Membership, MembershipAdmin)

admin.site.register(Record)