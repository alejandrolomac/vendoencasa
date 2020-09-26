from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.core.exceptions import ValidationError

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required=True
    
    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email')
        if password1 != password2:
            raise ValidationError("Las contraseñas no son iguales")
        if User.objects.filter(email=email).exists():
            raise ValidationError("El E-mail ya se utilizo en otra cuenta")
        return self.cleaned_data

class ProfileForm(forms.ModelForm):
    phone = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'99999999'}))

    class Meta:
        model = Profile
        fields = ('gender', 'Department', 'location', 'phone', 'code')
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['phone'].required=True
        self.fields['Department'].required=True
        self.fields['location'].required=True
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone == '':
            raise ValidationError("El teléfono es necesario para registrarse")
        elif isinstance(phone, int):
            raise ValidationError("El teléfono no debe contener letras o caracteres especiales ")
        return phone
    
    


class CreateCompanyForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required=True

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'resume', 'Department', 'location', 'phone', 'facebook', 'instagram', 'website', 'code')
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['name'].required=True
        self.fields['phone'].required=True
        self.fields['Department'].required=True
        self.fields['location'].required=True


class UserSettingForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class UserSettingProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['location', 'phone']