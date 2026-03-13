"""
URL configuration for myshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from shop.views import index, catalog, about, product_detail, privacy, terms, cookies
from shop.auth_views import register, user_login, user_logout, profile
from shop.cart_views import add_to_cart, cart_view, update_cart_item, remove_from_cart, cart_modal, clear_cart
from shop.checkout_views import checkout, order_success
from shop.review_views import add_review
from shop.admin_views import admin_panel, delete_review, delete_product, add_product, delete_reviews_bulk, edit_product, toggle_availability, order_detail
from shop.admin_views import close_order

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('catalog/', catalog, name='catalog'),
    re_path(r'^product/(?P<slug>[\w-]+)/$', product_detail, name='product_detail'),
    path('about/', about, name='about'),
    path('privacy/', privacy, name='privacy'),
    path('terms/', terms, name='terms'),
    path('cookies/', cookies, name='cookies'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('cart/', cart_view, name='cart'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', clear_cart, name='clear_cart'),
    path('cart/modal/', cart_modal, name='cart_modal'),
    path('checkout/', checkout, name='checkout'),
    path('order/success/', order_success, name='order_success'),
    path('review/add/<int:order_id>/', add_review, name='add_review'),
    path('admin-panel/', admin_panel, name='admin_panel'),
    path('admin-panel/review/delete/<int:review_id>/', delete_review, name='delete_review'),
    path('admin-panel/reviews/delete-bulk/', delete_reviews_bulk, name='delete_reviews_bulk'),
    path('admin-panel/product/delete/<int:product_id>/', delete_product, name='delete_product'),
    path('admin-panel/product/add/', add_product, name='add_product'),
    path('admin-panel/product/edit/<int:product_id>/', edit_product, name='edit_product'),
    path('admin-panel/product/toggle/<int:product_id>/', toggle_availability, name='toggle_availability'),
    path('admin-panel/order/<int:order_id>/', order_detail, name='order_detail'),
    path('close_order/<int:order_id>/', close_order, name='close_order'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
