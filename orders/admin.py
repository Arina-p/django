from django.contrib import admin

# Register your models here.
from orders.models import Order, OrderItem


class OrderItemTabulareAdmin(admin.TabularInline):
    model = OrderItem
    fields = "product", "price" # name
    search_fields = (
        "product",
        #"name",
    )
    extra = 0


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = "order", "product", "price"
    # search_fields = (
    #     "order",
    #     "product",
    #     "name",
    # )



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        #"requires_delivery",
        "status",
        "payment_on_get",
        #"is_paid",
        "created_timestamp",
    )

    search_fields = (
        "id",
    )
    readonly_fields = ("created_timestamp",)
    list_filter = (
        #"requires_delivery",
        "status",
        "payment_on_get",
        #"is_paid",
    )
    inlines = (OrderItemTabulareAdmin,)
