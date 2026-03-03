from django.shortcuts import render, get_object_or_404
from django.db import models
from .models import Product


def index(request):
    # Порядок слайдов
    slugs_order = ['tort-klassicheskiy', 'bento-tort', 'domashniy-zefir', 'goryachiy-shokolad', 'marshmellou', 'beze']
    featured_products = []
    
    for slug in slugs_order:
        product = Product.objects.filter(available=True, slug=slug).first()
        if product:
            featured_products.append(product)
    
    # Получаем последние 3 отзыва
    from .models import Review
    reviews = Review.objects.order_by('-created')[:3]
    return render(request, "index.html", {'featured_products': featured_products, 'reviews': reviews})


def catalog(request):
    dessert_types = [
        {'name': 'Торты', 'products': Product.objects.filter(dessert_type='Торты').exclude(slug='').order_by('-created')},
        {'name': 'Бенто', 'products': Product.objects.filter(dessert_type='Бенто').exclude(slug='').order_by('-created')},
        {'name': 'Горячий шоколад', 'products': Product.objects.filter(dessert_type='Горячий шоколад').exclude(slug='').order_by('-created')},
        {'name': 'Домашний зефир', 'products': Product.objects.filter(dessert_type='Домашний зефир').exclude(slug='').order_by('-created')},
        {'name': 'Маршмеллоу', 'products': Product.objects.filter(dessert_type='Маршмеллоу').exclude(slug='').order_by('-created')},
        {'name': 'Безе', 'products': Product.objects.filter(dessert_type='Безе').exclude(slug='').order_by('-created')},
    ]
    return render(request, "catalog.html", {"dessert_types": dessert_types})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, "product_detail.html", {'product': product})


def about(request):
    return render(request, "about.html")


def privacy(request):
    return render(request, "privacy.html")


def terms(request):
    return render(request, "terms.html")


def cookies(request):
    return render(request, "cookies.html")

def history(request):
    return render(request, "history.html")