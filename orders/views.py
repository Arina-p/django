
from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect, render
from carts.models import Cart

from orders.forms import CreateOrderForm, OrderItemForm
from orders.models import Order, OrderItem

from django.contrib.auth.decorators import login_required
from django.forms import formset_factory

@login_required
def create_order(request):
    OrderItemFormSet = formset_factory(OrderItemForm, extra=0)
    if request.method == 'POST':
        form = CreateOrderForm(data=request.POST)
        formset = OrderItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    user = request.user
                    cart_items = Cart.objects.filter(user=user)

                    if cart_items.exists():
                        order = Order.objects.create(
                            user=user,
                            payment_on_get=form.cleaned_data['payment_on_get'],
                        )
                        #for form in formset:
                        for form, cart_item in zip(formset, cart_items):
                            
                            membership_start_date = form.cleaned_data['membership_start_date']
                            product=cart_item.product
                            name=product.name
                            price=product.price
                            price=cart_item.product.price
                            quantity=cart_item.quantity
                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                price=product.price,  # Get the price from the product
                                quantity=quantity,
                                membership_start_date=membership_start_date,
                            )

                        cart_items.delete()
                        messages.success(request, 'Заказ оформлен!')
                        return redirect('users:profile')
            except ValidationError as e:
                messages.error(request, str(e))  # Using messages.error for better display
                return redirect('cart:order')
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }
        
        initial_data = [
            {}  # No initial data for OrderItemForm
            for item in Cart.objects.filter(user=request.user)
        ]
        formset = OrderItemFormSet(initial=initial_data)
        
        form = CreateOrderForm(initial=initial)

    context = {
        'title': 'Home - Оформление заказа',
        'form': form,
        'order': True,
        'formset': formset,  # Add the formset to the context
        'cart_items': Cart.objects.filter(user=request.user), # Add cart items to context
    
    }
    return render(request, 'orders/create_order.html', context=context)