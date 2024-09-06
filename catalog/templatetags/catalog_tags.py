from catalog.models import Category
from django import template

register = template.Library()

@register.simple_tag()
def tag_categories(): # по этому имени теперь можно вызвать функцию в шаблоне
    return Category.objects.all().order_by('id')
