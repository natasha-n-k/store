
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from .models import Product, Order, OrderItem
from .cart import Cart
from .forms import UserCreationForm, OrderCreateForm, CartAddProductForm
from django.contrib.auth.views import LoginView


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
            return redirect('shop:login')
    else:
        form = UserCreationForm()
        form.fields['username'].label = 'Имя пользователя'
        form.fields['username'].help_text = 'Обязательное поле. Максимум 150 символов. Разрешены буквы, цифры и символы @/./+/-/_'
        form.fields['email'].label = 'Email'
        form.fields['email'].help_text = 'Обязательное поле'
        form.fields['password1'].label = 'Пароль'
        form.fields['password1'].help_text = 'Ваш пароль не должен быть похож на другую личную информацию, должен содержать как минимум 8 символов, не может быть часто используемым паролем и не может состоять только из цифр.'
        form.fields['password2'].label = 'Подтверждение пароля'
        form.fields['password2'].help_text = 'Введите пароль, который вы ввели выше, для проверки.'
    return render(request, 'shop/signup.html', {'form': form})

@login_required
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
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {username}!')
            return redirect('shop:account_detail')  # перенаправляем на страницу личного кабинета
        else:
            error_message = 'Неверные имя пользователя или пароль'
            return render(request, 'shop/login.html', {'error_message': error_message})
    else:
        return render(request, 'shop/login.html')
    
def user_logout(request):
    logout(request)
    return redirect('shop:login')


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('shop:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('shop:cart_detail')