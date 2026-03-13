
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Order, Product, User, Review
from django.utils.text import slugify
from django.core.files.storage import default_storage
import os

@staff_member_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin_panel/order_detail.html', {'order': order})

@staff_member_required
def close_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.closed = True
    order.save()
    messages.success(request, f'Заказ {order.order_number} закрыт')
    return redirect('admin_panel')

@staff_member_required
def admin_panel(request):
    orders = Order.objects.filter(closed=False)[:10]
    @staff_member_required
    def close_order(request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order.closed = True
        order.save()
        messages.success(request, f'Заказ {order.order_number} закрыт')
        return redirect('admin_panel')
    products = Product.objects.all()
    reviews = Review.objects.all()
    
    stats = {
        'total_orders': Order.objects.count(),
        'total_products': Product.objects.count(),
        'total_users': User.objects.count(),
        'total_reviews': Review.objects.count(),
    }
    
    return render(request, 'admin_panel/dashboard.html', {
        'orders': orders,
        'products': products,
        'reviews': reviews,
        'stats': stats
    })

@staff_member_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    messages.success(request, 'Отзыв удален')
    return redirect('admin_panel')

@staff_member_required
def delete_reviews_bulk(request):
    if request.method == 'POST':
        review_ids = request.POST.getlist('review_ids')
        if review_ids:
            Review.objects.filter(id__in=review_ids).delete()
            messages.success(request, f'Удалено отзывов: {len(review_ids)}')
        else:
            messages.error(request, 'Выберите отзывы для удаления')
    return redirect('admin_panel')

@staff_member_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, 'Товар удален')
    return redirect('admin_panel')

@staff_member_required
def toggle_availability(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.available = not product.available
    product.save()
    status = 'в наличии' if product.available else 'снят с продажи'
    messages.success(request, f'Товар {status}')
    return redirect('admin_panel')

@staff_member_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        allergens = request.POST.get('allergens')
        weight = request.POST.get('weight')
        price = request.POST.get('price')
        dessert_type = request.POST.get('dessert_type')
        image_file = request.FILES.get('image')
        
        if not dessert_type:
            messages.error(request, 'Выберите тип десерта')
            return redirect('admin_panel')
        
        if image_file:
            file_name = f"images/{image_file.name}"
            file_path = os.path.join('static', file_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            
            slug = slugify(name, allow_unicode=True)
            if not slug:
                slug = f'product-{name[:20]}'
            if Product.objects.filter(slug=slug).exists():
                counter = 1
                while Product.objects.filter(slug=f"{slug}-{counter}").exists():
                    counter += 1
                slug = f"{slug}-{counter}"
            
            Product.objects.create(
                name=name,
                slug=slug,
                description=description,
                allergens=allergens,
                weight=weight,
                price=price,
                image=file_name,
                dessert_type=dessert_type,
                available=bool(request.POST.get('available'))
            )
            messages.success(request, 'Товар добавлен')
        else:
            messages.error(request, 'Необходимо загрузить изображение')
        
        return redirect('admin_panel')
    
    return redirect('admin_panel')

@staff_member_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.allergens = request.POST.get('allergens')
        product.weight = request.POST.get('weight')
        product.price = request.POST.get('price')
        product.dessert_type = request.POST.get('dessert_type')
        product.available = bool(request.POST.get('available'))
        
        discount_price = request.POST.get('discount_price')
        if discount_price:
            discount_price = float(discount_price)
            if discount_price >= float(product.price):
                messages.error(request, 'Цена со скидкой должна быть меньше обычной цены')
                return redirect('edit_product', product_id=product_id)
            product.discount_price = discount_price
        else:
            product.discount_price = None
        
        if not product.slug:
            new_slug = slugify(product.name, allow_unicode=True) or f'product-{product.id}'
            product.slug = new_slug
        
        if not product.dessert_type:
            messages.error(request, 'Выберите тип десерта')
            return redirect('edit_product', product_id=product_id)
        
        if request.POST.get('delete_image'):
            product.image = ''
        
        image_file = request.FILES.get('image')
        if image_file:
            file_name = f"images/{image_file.name}"
            file_path = os.path.join('static', file_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            product.image = file_name
        
        product.save(update_fields=['name', 'description', 'allergens', 'weight', 'price', 'discount_price', 'dessert_type', 'available', 'image', 'slug'])
        messages.success(request, 'Товар обновлен')
        return redirect('admin_panel')
    
    return render(request, 'admin_panel/edit_product.html', {'product': product})
