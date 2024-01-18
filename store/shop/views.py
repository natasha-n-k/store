
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from .models import Product, Order, OrderItem, Cart, UserCreationForm
from .forms import UserCreationForm, OrderCreateForm, CartAddProductForm
from django.contrib.auth.views import LoginView

def shop(request):
    return render(request, 'shop/shop.html') 

def product_list_1(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.all().order_by('-id')[:15]
    else:
        products = Product.objects.all().order_by('-id')[:15]

    page = request.GET.get('page', 1)
    paginator = Paginator(products, 9)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'shop/products_list_1.html', {'products': products})

from django.db.models import Count

def product_list_2(request):
    color_query = request.GET.get('color')
    size_query = request.GET.get('size')

    products = Product.objects.filter(category='clothing')

    if color_query:
        products = products.filter(color=color_query)

    if size_query:
        products = products.filter(size=size_query)

    color_counts = Product.objects.filter(category='clothing').values('color').annotate(count=Count('color')).order_by('color')
    size_counts = Product.objects.filter(category='clothing').values('size').annotate(count=Count('size')).order_by('size')

    page = request.GET.get('page', 1)
    paginator = Paginator(products, 9)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'color_counts': color_counts,
        'size_counts': size_counts
    }

    return render(request, 'shop/products_list_2.html', context)

def product_list_3(request):
    query = request.GET.get('q')
    color_query = request.GET.get('color')
    size_query = request.GET.get('size')

    products = Product.objects.filter(category='accessories')

    if query:
        products = products.filter(name__icontains=query)

    if color_query:
        products = products.filter(color=color_query)

    if size_query:
        products = products.filter(size=size_query)

    color_counts = products.values('color').annotate(count=Count('id')).order_by('color')
    size_counts = products.values('size').annotate(count=Count('id')).order_by('size')

    page = request.GET.get('page', 1)
    paginator = Paginator(products, 9)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'color_counts': color_counts,
        'size_counts': size_counts
    }

    return render(request, 'shop/products_list_3.html', context)


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    colors = product.color.split(',') if product.color else []
    sizes = product.size.split(',') if product.size else []
    return render(request, 'shop/product_detail.html', {'product': product, 'colors': colors, 'sizes': sizes})

@login_required
def cart_detail(request):
    cart = Cart.objects.filter(user=request.user).all()

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        if product_id and action:
            try:
                cart_item = Cart.objects.get(user=request.user, id=product_id)
                if action == 'delete':
                    cart_item.delete()
                elif action == 'update':
                    quantity = int(request.POST.get('quantity'))
                    cart_item.quantity = quantity
                    cart_item.save()
            except Cart.DoesNotExist:
                pass

    context = {
        'cart': cart,
    }
    return render(request, 'shop/cart_detail.html', context)


@login_required
def account_detail(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'shop/account_detail.html', {'orders': orders})
    
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('shop:login')
        else:
            for field_name, errors in form.errors.items():
                for error in errors:
                    messages.warning(request, f"Ошибка в поле '{form.fields[field_name].label}': {error}")
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
@require_POST
def order_create(request):
    cart = Cart.objects.filter(user=request.user)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                    color=item.color, 
                    size=item.size, 
                )
            cart.delete()
            return redirect(reverse('shop:order_history', args=[order.id]))
    else:
        form = OrderCreateForm()
    return render(request, 'shop/checkout.html', {'form': form, 'cart': cart})

@csrf_protect
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {username}!')
            if request.user.is_authenticated:  # проверяем, авторизован ли пользователь
                return redirect('shop:account_detail')  # если авторизован, перенаправляем на страницу личного кабинета
            else:
                return redirect('shop:login')  # если не авторизован, перенаправляем на страницу входа
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
    product = Product.objects.get(id=product_id)
    color = request.POST.get('color')
    size = request.POST.get('size')
    cart = Cart.objects.filter(user=request.user, product=product, color=color, size=size).first()
    if cart:
        cart.quantity += 1
        cart.save()
    else:
        cart = Cart.objects.create(user=request.user, product=product, color=color, size=size)
    return redirect('shop:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('shop:cart_detail')

@login_required
def order_history(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'shop/order_history.html', {'order': order})