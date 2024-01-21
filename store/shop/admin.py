from django.contrib import admin
from .models import Product, Order, OrderItem, Cart, Color, Size

class ColorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

admin.site.register(Color, ColorAdmin)

class SizeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

admin.site.register(Size, SizeAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price']
    list_filter = ['colors', 'sizes', 'category']
    search_fields = ['name', 'description', 'colors__name', 'sizes__name']
    filter_horizontal = ['colors', 'sizes']  # This will make it easier to select multiple colors and sizes

admin.site.register(Product, ProductAdmin)

# регистрация модели OrderItem
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

# регистрация модели Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'paid']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]

# регистрация модели Cart
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']

