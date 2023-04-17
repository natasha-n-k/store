from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Order


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)
    color = forms.CharField(max_length=50)
    size = forms.CharField(max_length=10)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
