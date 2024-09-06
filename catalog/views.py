from django.shortcuts import get_list_or_404, render
from catalog.models import Category, Product

def catalog(request, category_slug):
    
    if category_slug == 'all':
        goods = Product.objects.all()
    else:
        goods = get_list_or_404(Product.objects.filter(category__slug=category_slug))
    
    
    context = {
        'title': 'Каталог',
        'goods': goods ,
        'slug_url': category_slug
    }
    return render(request, 'catalog/catalog.html', context)



