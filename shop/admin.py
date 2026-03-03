from django.contrib import admin
from .models import Product, Cart, CartItem, Order, OrderItem, Review


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'dessert_type', 'price', 'available', 'created']
    list_filter = ['available', 'created', 'dessert_type']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created', 'get_total_price']
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'get_total_price']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'total_price', 'created']
    list_filter = ['created']
    search_fields = ['order_number', 'user__username']
    inlines = [OrderItemInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating', 'created', 'order']
    list_filter = ['rating', 'created']
    search_fields = ['user__username', 'comment']
