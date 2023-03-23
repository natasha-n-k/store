
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Product, Order, OrderItem
from .forms import UserCreationForm, OrderCreateForm, CartAddProductForm
from .cart import Cart



def shop(request):
    return render(request, 'shop/shop.html') 

def product_list_1(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    else:
        products = Product.objects.all()
    return render(request, 'shop/products_list_1.html', {'products': products})

def product_list_2(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    else:
        products = Product.objects.all()
    return render(request, 'shop/products_list_2.html', {'products': products})

def product_list_3(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    else:
        products = Product.objects.all()
    return render(request, 'shop/products_list_3.html', {'products': products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required
def cart_detail(request):
    order = Order.objects.filter(user=request.user, paid=False).first()
    if order:
        order_items = order.items.all()
    else:
        order_items = []
    return render(request, 'shop/cart_detail.html', {'order_items': order_items, 'order': order})

@login_required
def account_detail(request):
    return render(request, 'shop/account_detail.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('shop:index')
    else:
        form = UserCreationForm()
    return render(request, 'shop/signup.html', {'form': form})

@login_required
def order_create(request):
    order = Order.objects.filter(user=request.user, paid=False).first()
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.user = request.user
            new_order.order = order
            new_order.save()
            for item in order.items.all():
                new_item = OrderItem.objects.create(order=new_order, product=item.product, quantity=item.quantity)
                new_item.save()
            order.ordered = True
            order.save()
            return redirect('shop:index')
    else:
        form = OrderCreateForm()
    return render(request, 'shop/checkout.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('shop:index')
        else:
            return render(request, 'shop/login.html', {'error': 'Invalid login credentials'})
    else:
        return render(request, 'shop/login.html')
    
def user_logout(request):
    logout(request)
    return redirect('shop:index')

@require_POST
def cart_add(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('shop:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.remove(product)
    return redirect('shop:cart_detail')