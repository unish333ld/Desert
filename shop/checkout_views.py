from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, Order, OrderItem
import random
import string


@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    
    if not cart.items.exists():
        return redirect('cart')
    
    if request.method == 'POST':
        # Генерируем уникальный номер заказа
        order_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        
        # Создаем заказ
        order = Order.objects.create(
            user=request.user,
            order_number=order_number,
            total_price=cart.get_total_price()
        )
        
        # Копируем товары из корзины в заказ
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product_name=item.product.name,
                product_price=item.product.price,
                quantity=item.quantity
            )
        
        # Очищаем корзину
        cart.items.all().delete()
        return redirect('order_success')
    
    return render(request, 'cart/checkout.html', {'cart': cart})


@login_required
def order_success(request):
    return render(request, 'cart/order_success.html')
