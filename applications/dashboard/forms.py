from django.forms import ModelForm
from django import forms
from applications.product.models import Products

class ProductForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    price = forms.CharField(max_length=30)
    imagef = forms.ImageField(max_length=30)
    class Meta:
        model = Products
        fields = ('title', 'company', 'subCategory', 'resume', 'imagef', 'images', 'imaget', 'price', 'priceAnchor', 'pricePromo', 'promotion', 'exhausted', 'colors', 'sizes')
    
    def clean(self):
        cleaned_data = super(ProductForm, self).clean()
        title = cleaned_data.get('title')
        price = cleaned_data.get('price')
        imagef = cleaned_data.get('imagef')