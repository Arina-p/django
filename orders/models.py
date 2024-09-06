from django.db import models
from catalog.models import Product
from users.models import User



class OrderitemQueryset(models.QuerySet):
    
    def total_price(self):
        return sum(cart.products_price() for cart in self)
    


class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, blank=True, null=True, verbose_name="Пользователь", default=None)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заказа")
    payment_on_get = models.BooleanField(default=True, verbose_name="Оплата при получении")
    status = models.CharField(max_length=50, default='В обработке', verbose_name="Статус заказа")

    
    

    class Meta:
        db_table = "order"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ № {self.pk} | Покупатель {self.user.first_name} {self.user.last_name}"



class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(to=Product, on_delete=models.SET_DEFAULT, null=True, verbose_name="Товар", default=None)
   
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    membership_start_date = models.DateField(null=True, blank=True, verbose_name="Дата начала действия абонемента")


    class Meta:
        db_table = "order_item"
        verbose_name = "Проданный товар"
        verbose_name_plural = "Проданные товары"

    objects = OrderitemQueryset.as_manager()

    def products_price(self):
        return self.price # self.product.price

    def __str__(self):
        return f"Заказ № {self.order.pk} часть {self.pk}| товар {self.product} | покупатель {self.order.user}"
        

