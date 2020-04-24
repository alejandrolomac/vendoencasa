from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CreateUserForm, ProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction

@transaction.atomic
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('product_app:index')
    else:
        if request.method == 'POST':
            form = CreateUserForm(data=request.POST)
            profile_form = ProfileForm(data=request.POST)
            if form.is_valid() and profile_form.is_valid():
                user = form.save(commit=False)
                user.save()
                
                profile = profile_form.save(commit=False)
                profile.user = user
                #profile.save()

                messages.success(request, "Se ha creado tu cuenta " + str(user))
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect("product_app:index")
        else:
            form = CreateUserForm()
            profile_form = ProfileForm()

        return render(request, 'registration/register.html', {
            'form':form,
            'profile_form':profile_form
        })

def loginPage(request):
    form = AuthenticationForm()
    if request.user.is_authenticated:
        return redirect('product_app:index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('product_app:index')
                messages.success(request, "Bienvenido " + user)
            else:
                messages.error(request, "Usuario o Contraseña Incorrecto")

        context = {'form':form}
        return render(request, 'registration/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect("useradmin_app:entrar")