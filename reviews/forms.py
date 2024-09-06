from django import forms
from .models import Review
from users.models import User
from django.contrib.auth.models import Group
import re

class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = Review
        
        fields = ['rating', 'review_text']
        
    def clean_review_text(self):
        review_text = self.cleaned_data['review_text']
        
        # Удаление тегов HTML
        clean_text = re.sub(r'<[^>]+>', '', review_text)

        # Удаление URL-ссылок
        clean_text = re.sub(r'https?://\S+', '', clean_text)
        if not clean_text:
            raise forms.ValidationError("Отзыв не должен быть пустым")
        return clean_text
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
    
