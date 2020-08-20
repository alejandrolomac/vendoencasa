from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('gender', 'location', 'phone')


class CreateCompanyForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'resume', 'location', 'phone', 'logo', 'facebook', 'instagram', 'website')


class UserSettingForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class UserSettingProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['location', 'phone']