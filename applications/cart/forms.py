from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User
from applications.cart.models import Order, OrderItem

class OrderForm(forms.Form):
    orderLocation = forms.CharField(label='Dirección asd', max_length=100)