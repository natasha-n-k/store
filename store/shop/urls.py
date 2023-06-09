"""test_project URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from . import views
from django.contrib.auth.views import LoginView

app_name = 'shop'

urlpatterns = [
    path('', views.shop, name='shop'),
    path('products_1/', views.product_list_1, name='product_list_1'),
    path('products_2/', views.product_list_2, name='product_list_2'),
    path('products_3/', views.product_list_3, name='product_list_3'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('order/', views.order_create, name='order_create'),
    path('checkout/', views.order_create, name='checkout'),
    path('account/', views.account_detail, name='account_detail'),
    path('login/', LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('order_history/<int:order_id>/', views.order_history, name='order_history'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)