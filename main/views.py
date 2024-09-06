from django.shortcuts import render
from django.http import HttpResponse
from reviews.models import Review

# Create your views here.
def index(request):
    sort_by = request.GET.get('sort_by', 'review_date')
    reviews = Review.objects.all().order_by(sort_by)

    data = {
        'title': 'Главная страница', # в шаблоне {{title}}, передаем для каждой стр разный но тогда непонятно, как в классах
        'reviews': reviews
    }
    return render(request, 'main/index.html', data)