# Generated by Django 5.0.2 on 2024-05-11 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_orderitem_membership_start_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_on_get',
            field=models.BooleanField(default=True, verbose_name='Оплата при получении'),
        ),
    ]
