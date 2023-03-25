
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Product, Order, OrderItem
from .cart import Cart
from .forms import UserCreationForm, OrderCreateForm, CartAddProductForm


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


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart_detail.html', {'cart': cart})

@login_required
def account_detail(request):
    return render(request, 'shop/account_detail.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'shop/signup.html', {'form': form})

def order_create(request):
    order = Order.objects.filter(user=request.user, paid=False).first()
    if order is None:
        # create a new order if one doesn't exist
        order = Order.objects.create(user=request.user, paid=False)
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
            return redirect('shop:shop')
    else:
        form = OrderCreateForm()
    return render(request, 'shop/checkout.html', {'form': form})

@csrf_protect
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('shop:account_detail')
        else:
            return render(request, 'shop/login.html', {'error': 'Invalid login credentials'})
    else:
        return render(request, 'shop/login.html')
    
def user_logout(request):
    logout(request)
    return redirect('shop:login')

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = request.POST.get('quantity')
    if quantity is not None:
        cart.add(product=product, quantity=quantity, update_quantity=request.POST.get('update', False))
    return redirect('shop:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product=product)
    return redirect('shop:cart_detail')