from django.shortcuts import render, redirect
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from datetime import date

@login_required
def add_review(request):

    if request.method == 'POST':
        
        form = ReviewForm(request.POST) # data=
        
        if form.is_valid():
            review = form.save(commit=False)
            
            review.user = request.user  # Автоматически устанавливаем текущего пользователя
            review.review_date = date.today()
            print(review)
            review.save()
            
            return redirect('main:home')  # Перенаправляем на страницу успеха home#reviews
        else:
            
            return render(request, 'main/index.html', {'form': form})
    else:
        form = ReviewForm()
    return render(request, 'main/index.html', {'form': form})