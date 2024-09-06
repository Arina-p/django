from django import forms
from catalog.models import Product
from django.core.validators import MinValueValidator
from datetime import date

class CreateOrderForm(forms.Form):

    first_name = forms.CharField()
    last_name = forms.CharField()
    
    payment_on_get = forms.ChoiceField(
        choices=[
            ("1", 'True'),
            ],
        )
    
class MembershipItemForm(forms.Form):
    cart_item_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(min_value=1)
    membership_start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

class OrderItemForm(forms.Form):
    
    membership_start_date = forms.DateField(
        widget=forms.SelectDateWidget(), label="Дата начала действия",
        initial=date.today,  # Set today as the default value
        validators=[MinValueValidator(date.today)],
        )
