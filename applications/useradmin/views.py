from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .forms import CreateUserForm, ProfileForm, CompanyForm, CreateCompanyForm, UserSettingForm, UserSettingProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from applications.useradmin.models import Profile
from applications.cart.models import Order, OrderItem
from applications.product.models import RegistrationCode
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def registerDefault(request):
    context = {}
    return render(request, 'registration/register.html', context)

@transaction.atomic
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('product_app:index')
    else:
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            profile_form = ProfileForm(request.POST)
            if form.is_valid() and profile_form.is_valid():
                user = form.save()
                user.profile.gender = profile_form.cleaned_data['gender']
                user.profile.location = profile_form.cleaned_data['location']
                user.profile.phone = profile_form.cleaned_data['phone']
                user.profile.code = profile_form.cleaned_data['code']
                user.profile.save()
                user.save()
                
                #:::::: EMAIL ::::::
                title = 'Bienvenido a Vendo en Casa'
                to = user.email
                html_content = render_to_string('welcome_email.html', {'title': title})
                text_content = strip_tags(html_content)
                email = EmailMultiAlternatives(
                    title,
                    text_content,
                    settings.EMAIL_HOST_USER,
                    [to]
                )
                email.attach_alternative(html_content, "text/html")
                email.send()
                #:::::: EMAIL ::::::
                messages.success(request, "¡Gracias por unirte!")
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect("product_app:index")
        else:
            form = CreateUserForm()
            profile_form = ProfileForm()

        return render(request, 'registration/register-usuario.html', {
            'form':form,
            'profile_form':profile_form
        })

def loginDefault(request):
    context = {}
    return render(request, 'registration/login.html', context)

def loginPage(request):
    form = AuthenticationForm()
    if request.user.is_authenticated:
        return redirect('dashboard_app:dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard_app:dashboard')
                messages.success(request, "Bienvenido " + user)
            else:
                messages.error(request, "Usuario o Contraseña Incorrecto")

        context = {'form':form}
        return render(request, 'registration/login-company.html', context)

def loginUsuarios(request):
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
        return render(request, 'registration/login-user.html', context)


def logoutUser(request):
    logout(request)
    return redirect("useradmin_app:entrar")


@transaction.atomic
def registerCompany(request):
    if request.user.is_authenticated:
        return redirect('dashboard_app:dashboard')
    else:
        if request.method == 'POST':
            form = CreateCompanyForm(request.POST)
            company_form = CompanyForm(request.POST, request.FILES)
            if form.is_valid() and company_form.is_valid():
                user = form.save()
                user.profile.location = company_form.cleaned_data['location']
                user.profile.phone = company_form.cleaned_data['phone']
                user.profile.name = company_form.cleaned_data['name']
                user.profile.resume = company_form.cleaned_data['resume']
                #user.profile.logo = company_form.cleaned_data['logo']
                user.profile.plan = 'Vendedor'
                permission = Permission.objects.get(name='Can add products')
                user.user_permissions.add(permission)
                user.profile.save()
                user.save()

                #:::::: EMAIL ::::::
                title = 'Bienvenido a Vendo en Casa'
                to = user.email
                html_content = render_to_string('welcome_email_company.html', {'title': title})
                text_content = strip_tags(html_content)
                email = EmailMultiAlternatives(
                    title,
                    text_content,
                    settings.EMAIL_HOST_USER,
                    [to]
                )
                email.attach_alternative(html_content, "text/html")
                email.send()
                #:::::: EMAIL ::::::

                messages.success(request, "¡Gracias por unirte!")
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect("dashboard_app:dashboard")
        else:
            form = CreateCompanyForm()
            company_form = CompanyForm()

        return render(request, 'registration/register-company.html', {
            'form':form,
            'company_form':company_form
        })

@login_required(login_url='useradmin_app:entrar')
def perfil(request):
    acode = RegistrationCode.objects.all().filter(associated=request.user.id)
    if acode:
        affiliatecode = RegistrationCode.objects.get(associated=request.user.id)
        affiliates = Profile.objects.all().filter(code=affiliatecode).count()
    else:
        affiliatecode = ''
        affiliates = ''

    ncorder = Order.objects.all().filter(user=request.user.id, status='NoPagados')
    if ncorder:
        order = Order.objects.get(user=request.user.id, status='NoPagados')
    else:
        order = ''
    
    pcorder = Order.objects.all().filter(user=request.user.id, status='Procesando')
    if pcorder:
        porder = Order.objects.get(user=request.user.id, status='Procesando')
    else:
        porder = ''
    
    ecorder = Order.objects.all().filter(user=request.user.id, status='Enviado')
    if ecorder:
        eorder = Order.objects.get(user=request.user.id, status='Enviado')
    else:
        eorder = ''
    
    pacorder = Order.objects.all().filter(user=request.user.id, status='Pagado')
    if pacorder:
        pagorder = Order.objects.get(user=request.user.id, status='Pagado')
    else:
        pagorder = ''
    
    cocorder = Order.objects.all().filter(user=request.user.id, status='Comentado')
    if cocorder:
        comeorder = Order.objects.get(user=request.user.id, status='Comentado')
    else:
        comeorder = ''

    product_to_edit = get_object_or_404(User, pk=request.user.id)
    profile_to_edit = get_object_or_404(Profile, user=request.user.id)
    form = UserSettingForm(instance=product_to_edit)
    formp = UserSettingProfileForm(instance=profile_to_edit)
    if request.method == 'POST':
        form = CreateCompanyForm(request.POST, request.FILES, instance=product_to_edit)
        formp = CompanyForm(instance=profile_to_edit)
        if form.is_valid():
            form.save()
            formp.save()
            return redirect('useradmin_app:perfil')
        else:
            form = CreateCompanyForm(instance=product_to_edit)
            formp = CompanyForm(instance=profile_to_edit)

    return render(request, "perfil.html", {'form': form, 'formp': formp, 'product': product_to_edit, 'affiliatecode': affiliatecode, 'affiliates': affiliates, 'order': order, 'porder': porder, 'eorder': eorder, 'pagorder': pagorder, 'comeorder': comeorder})
