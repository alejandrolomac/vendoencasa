from django.forms import ModelForm
from django import forms
from applications.product.models import Products

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ('title', 'company', 'subCategory', 'resume', 'imagef', 'images', 'imaget', 'price', 'priceAnchor', 'pricePromo', 'promotion', 'exhausted', 'colors', 'sizes')