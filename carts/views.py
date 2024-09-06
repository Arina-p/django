from django.shortcuts import redirect, render
from carts.models import Cart

from catalog.models import Product
from carts.utils import get_user_carts
from django.http import JsonResponse
from django.template.loader import render_to_string


def cart_add(request):

    product_id = request.POST.get("product_id")

    product = Product.objects.get(id=product_id)
    
    if request.user.is_authenticated:

        Cart.objects.create(user=request.user, product=product, quantity=1)

    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_cart}, request=request)

    response_data = {
        "message": "Товар добавлен в корзину",
        "cart_items_html": cart_items_html,
    }

    return JsonResponse(response_data)
            



def cart_remove(request):
    
    cart_id = request.POST.get("cart_id")

    cart = Cart.objects.get(id=cart_id)
    cart.delete()

    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_cart}, request=request)

    response_data = {
        "message": "Товар удален",
        "cart_items_html": cart_items_html,
    }

    return JsonResponse(response_data)