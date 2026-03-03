from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Product, Cart, CartItem


@login_required
def add_to_cart(request, product_id):
    if request.user.is_superuser:
        messages.error(request, 'Администратор не может добавлять товары в корзину')
        return redirect('catalog')
    
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, 'Товар добавлен в корзину!', extra_tags='cart_success')
    return redirect('catalog')


@login_required
def cart_view(request):
    if request.user.is_superuser:
        return redirect('admin_panel')
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cart.html', {'cart': cart})


@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    action = request.POST.get('action')
    
    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart = cart_item.cart if cart_item.id else Cart.objects.get(user=request.user)
        return JsonResponse({
            'success': True,
            'quantity': cart_item.quantity if cart_item.id else 0,
            'item_total': float(cart_item.get_total_price()) if cart_item.id else 0,
            'cart_total': float(cart.get_total_price())
        })
    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart = Cart.objects.get(user=request.user)
        return JsonResponse({'success': True, 'cart_total': float(cart.get_total_price())})
    return redirect('cart')


@login_required
def cart_modal(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cart_modal.html', {'cart': cart})


@login_required
def clear_cart(request):
    cart = Cart.objects.get(user=request.user)
    cart.items.all().delete()
    return redirect('cart')
