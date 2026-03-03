from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = 'От 6 до 16 символов. Буквы и цифры.'
        self.fields['password2'].help_text = 'Повторите пароль'
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 4:
            raise ValidationError('Имя должно быть не менее 4 символов')
        if not re.match(r'^[a-zA-Zа-яА-Я0-9]+$', username):
            raise ValidationError('Имя может содержать только буквы (русские/английские) и цифры')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Это имя пользователя уже занято')
        return username
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 6:
            raise ValidationError('Пароль должен быть не менее 6 символов')
        if len(password) > 16:
            raise ValidationError('Пароль должен быть не более 16 символов')
        if not re.match(r'^[a-zA-Zа-яА-Я0-9]+$', password):
            raise ValidationError('Пароль может содержать только буквы (русские/английские) и цифры')
        return password
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Пароли не совпадают')
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
