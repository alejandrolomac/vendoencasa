from django.forms import ModelForm
from django import forms
from applications.product.models import Products, Color, Size
from django.forms.widgets import CheckboxSelectMultiple

class ProductForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Nombre del producto'}))
    price = forms.FloatField(widget=forms.TextInput(attrs={'placeholder':'Precio'}))
    pricePromo = forms.FloatField(widget=forms.TextInput(attrs={'placeholder':'Precio Promoción', 'class':'mt-2'}))
    resume = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Descripción del producto', 'class':'mt-3'}))
    
    class Meta:
        model = Products
        fields = ('title', 'company', 'subCategory', 'imagef', 'images', 'imaget', 'price', 'pricePromo', 'promotion', 'colors', 'resume', 'sizes', 'available')
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['pricePromo'].required=False
        self.fields["colors"].widget = CheckboxSelectMultiple()
        self.fields["colors"].queryset = Color.objects.all()
        self.fields["sizes"].widget = CheckboxSelectMultiple()
        self.fields["sizes"].queryset = Size.objects.all()