from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.files.storage import FileSystemStorage


fs = FileSystemStorage(location='media/product_images')



class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY_CHOICES = (
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Clothing', null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images')
    colors = models.ManyToManyField(Color)
    sizes = models.ManyToManyField(Size)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-id']

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=255)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Заказ {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    color = models.CharField(max_length=50, default='Белый', null=True)
    size = models.CharField(max_length=20, default='One',null=True)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=50, default='Белый', null=True)
    size = models.CharField(max_length=20, default='One',null=True)

    def get_total_price(self):
        return self.product.price * self.quantity
    
    def get_cart_total(self):
        return sum(item.get_total_price() for item in Cart.objects.filter(user=self.user))