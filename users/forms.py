from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from captcha.fields import CaptchaField
from django.contrib.auth.models import Group

class DateInput(forms.DateInput):
    input_type = 'date'

class LoginUserForm(AuthenticationForm): # forms.Form для функции login_user
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-input'})) # attrs: 'placeholder': '', 'autofocus': True
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'})) # 'autocomplete': 'current_password'
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-input'})) # стили добавили после
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'})) # password
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    captcha = CaptchaField()
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'patronymic', 'date_birth', 'phone', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия', # ""
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'date_birth': DateInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'В формате: XXX-XXX-XX-XX'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email') # email = self.cleaned_data в примере, но ошибка
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такой email уже существует")
        return email

        
 

class UserGroupForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label=None)

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'patronymic', 'email', 'group', 'is_staff' ]