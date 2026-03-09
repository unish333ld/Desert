from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import Cart, Order


def register(request):
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Регистрация прошла успешно!')
                return redirect('index')
            except:
                messages.error(request, 'username:Это имя пользователя уже занято')
                return redirect('register')
        else:
            request.session['form_data'] = {
                'username': request.POST.get('username', ''),
                'email': request.POST.get('email', ''),
                'password1': request.POST.get('password1', ''),
                'password2': request.POST.get('password2', '')
            }
            
            # Сначала проверяем ошибки валидации формы
            if 'username' in form.errors:
                messages.error(request, f'username:{form.errors["username"][0]}')
            elif 'email' in form.errors:
                messages.error(request, f'email:{form.errors["email"][0]}')
            elif 'password1' in form.errors:
                messages.error(request, f'password1:{form.errors["password1"][0]}')
            elif 'password2' in form.errors:
                messages.error(request, f'password2:{form.errors["password2"][0]}')
            # Затем проверяем пустые поля
            elif not request.POST.get('email'):
                messages.error(request, 'email:Введите email')
            elif not request.POST.get('password1'):
                messages.error(request, 'password1:Введите пароль')
            elif not request.POST.get('password2'):
                messages.error(request, 'password2:Подтвердите пароль')
            else:
                messages.error(request, 'password1:Проверьте правильность заполнения')
            return redirect('register')
    else:
        form = CustomUserCreationForm()
    
    form_data = request.session.pop('form_data', {})
    return render(request, 'accounts/register.html', {'form': form, 'form_data': form_data})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
        else:
            request.session['form_data'] = {'username': request.POST.get('username', '')}
            if not request.POST.get('username'):
                messages.error(request, 'username:Введите имя пользователя')
            elif not request.POST.get('password'):
                messages.error(request, 'password:Введите пароль')
            else:
                messages.error(request, 'password:Неверное имя пользователя или пароль')
            return redirect('login')
    else:
        form = AuthenticationForm()
    
    form_data = request.session.pop('form_data', {})
    return render(request, 'accounts/login.html', {'form': form, 'form_data': form_data})


def user_logout(request):
    logout(request)
    return redirect('index')


@login_required
def profile(request):
    if request.user.is_superuser:
        return redirect('admin_panel')
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    orders = Order.objects.filter(user=request.user)
    return render(request, 'accounts/profile.html', {'cart': cart, 'orders': orders})
