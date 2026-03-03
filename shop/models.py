from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Product(models.Model):
    DESSERT_TYPES = [
        ('Торты', 'Торты'),
        ('Бенто', 'Бенто'),
        ('Горячий шоколад', 'Горячий шоколад'),
        ('Домашний зефир', 'Домашний зефир'),
        ('Маршмеллоу', 'Маршмеллоу'),
        ('Безе', 'Безе'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    description = models.TextField(verbose_name='Описание')
    allergens = models.TextField(blank=True, verbose_name='Аллергены')
    weight = models.IntegerField(null=True, blank=True, verbose_name='Вес (в граммах)')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Цена со скидкой')
    image = models.CharField(max_length=200, verbose_name='Изображение')
    dessert_type = models.CharField(max_length=50, choices=DESSERT_TYPES, default='Торты', verbose_name='Тип десерта')
    available = models.BooleanField(default=True, verbose_name='Доступен')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])
    
    def get_price(self):
        return self.discount_price if self.discount_price else self.price
    



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
    
    def __str__(self):
        return f'Корзина {self.user.username}'
    
    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE, verbose_name='Корзина')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    
    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
    
    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
    
    def get_total_price(self):
        return self.product.get_price() * self.quantity


class Order(models.Model):
    closed = models.BooleanField(default=False, verbose_name='Закрыт')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    order_number = models.CharField(max_length=20, unique=True, verbose_name='Номер заказа')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created']
    
    def __str__(self):
        return f'Заказ {self.order_number}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Заказ')
    product_name = models.CharField(max_length=200, verbose_name='Название товара')
    product_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    
    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'
    
    def __str__(self):
        return f'{self.quantity} x {self.product_name}'
    
    def get_total_price(self):
        return self.product_price * self.quantity


class Review(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.PositiveIntegerField(verbose_name='Оценка')
    comment = models.TextField(verbose_name='Комментарий')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created']
    
    def __str__(self):
        return f'Отзыв от {self.user.username}'
