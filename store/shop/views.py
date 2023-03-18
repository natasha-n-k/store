from django.shortcuts import render

# Create your views here.
def shop(request):

    return render(request, 'shop/shop.html')

def product_list_1(request):
    #products = Product.objects.all()
    #context = {'products': products}
    return render(request, 'shop/product_list_1.html')

def product_list_2(request):
    #products = Product.objects.all()
    #context = {'products': products}
    return render(request, 'shop/products_list_2.html')

def product_list_3(request):
    #products = Product.objects.all()
    #context = {'products': products}
    return render(request, 'shop/products_list_3.html')

def product_detail(request, pk):
    #product = Product.objects.get(pk=pk)
    #context = {'product': product}
    return render(request, 'shop/products_detail.html')

def cart_detail(request):
    context = {}
    return render(request, 'shop/cart_detail.html')

def account_detail(request):
    context = {}
    return render(request, 'shop/account_detail.html')

def login(request):
    context = {}
    return render(request, 'shop/login.html')

def signup(request):
    context = {}
    return render(request, 'shop/signup.html')

def checkout(request):
    context = {}
    return render(request, 'shop/checkout.html')