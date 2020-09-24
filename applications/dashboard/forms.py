from django.forms import ModelForm
from django import forms
from applications.product.models import Products, Color, Size, SubCategory
from django.forms.widgets import CheckboxSelectMultiple
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from applications.useradmin.models import Profile
from applications.orders.models import OrdersProducts

class ProductForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Nombre del producto'}))
    price = forms.FloatField(widget=forms.TextInput(attrs={'placeholder':'Precio'}))
    pricePromo = forms.FloatField(widget=forms.TextInput(attrs={'placeholder':'Precio Promoción', 'class':'mt-2'}))
    resume = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Descripción del producto', 'class':'mt-3'}))
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'Cantidad'}))
    
    class Meta:
        model = Products
        fields = ('title', 'subCategory', 'imagef', 'images', 'imaget', 'price', 'pricePromo', 'promotion', 'colors', 'resume', 'sizes', 'available', 'quantity', 'statusproduct')
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['pricePromo'].required=False
        self.fields["colors"].widget = CheckboxSelectMultiple()
        self.fields["colors"].queryset = Color.objects.all()
        self.fields["sizes"].widget = CheckboxSelectMultiple()
        self.fields["sizes"].queryset = Size.objects.all()
        self.fields["subCategory"].queryset = SubCategory.objects.all().order_by('name')



class CreateCompanyForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'resume', 'location', 'phone', 'logo', 'facebook', 'instagram', 'website')

class OrdersForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Nombre del producto'}))
    price = forms.FloatField(widget=forms.TextInput(attrs={'placeholder':'Precio'}))
    pricePromo = forms.FloatField(widget=forms.TextInput(attrs={'placeholder':'Precio Promoción', 'class':'mt-2'}))
    resume = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Descripción del producto', 'class':'mt-3'}))
    
    class Meta:
        model = OrdersProducts
        fields = ('title', 'subCategory', 'imagef', 'images', 'imaget', 'price', 'pricePromo', 'promotion', 'colors', 'resume', 'sizes', 'available')
    
    def __init__(self, *args, **kwargs):
        super(OrdersForm, self).__init__(*args, **kwargs)
        self.fields['pricePromo'].required=False
        self.fields["colors"].widget = CheckboxSelectMultiple()
        self.fields["colors"].queryset = Color.objects.all()
        self.fields["sizes"].widget = CheckboxSelectMultiple()
        self.fields["sizes"].queryset = Size.objects.all()