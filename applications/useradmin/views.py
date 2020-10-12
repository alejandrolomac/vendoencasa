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
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

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
                emailcheck = form.cleaned_data.get('email')
                emailexist = User.objects.all().filter(email=emailcheck)
                if emailexist:
                    messages.error(request, "Ya se utilizo este E-Mail")
                elif len(form.cleaned_data.get('password1')) <= 6:
                    messages.error(request, "La contraseña debe tener al menos 6 caracteres")
                else:
                    user = form.save()
                    user.profile.gender = profile_form.cleaned_data['gender']
                    user.profile.Department = profile_form.cleaned_data['Department']
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
                usercheck = request.POST.get('username')
                userexist = User.objects.filter(username=usercheck)
                if userexist:
                    messages.error(request, "Ya se utilizo este Usuario")

                if len(form.cleaned_data.get('password1')) <= 6:
                    messages.error(request, "La contraseña debe tener al menos 6 caracteres")
                elif form.cleaned_data.get('password1') != form.cleaned_data.get('password2'):
                    messages.error(request, "Las contraseñas son diferentes")
        else:
            form = CreateUserForm()
            profile_form = ProfileForm()
            messages.info(request, "¡Estas a punto de formar parte de la mejor plataforma del país!")

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

            userexist = User.objects.filter(username=username)
            useremailexist = User.objects.filter(email=username)

            if useremailexist:
                user = authenticate(request, username=User.objects.get(email=username).username, password=password)
            else:
                user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard_app:dashboard')
                messages.success(request, "Bienvenido " + user)
            elif not '@' in username and not userexist:
                messages.error(request, "Usuario Incorrecto")
            elif '@' in username and not useremailexist:
                messages.error(request, "E-mail Incorrecto")
            else:
                messages.error(request, "Password Incorrecto")

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
            
            userexist = User.objects.filter(username=username)
            useremailexist = User.objects.filter(email=username)

            if useremailexist:
                user = authenticate(request, username=User.objects.get(email=username).username, password=password)
            else:
                user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('product_app:index')
                messages.success(request, "Bienvenido " + user)
            elif not '@' in username and not userexist:
                messages.error(request, "Usuario Incorrecto")
            elif '@' in username and not useremailexist:
                messages.error(request, "E-mail Incorrecto")
            else:
                messages.error(request, "Password Incorrecto")

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
                emailcheck = form.cleaned_data.get('email')
                emailexist = User.objects.all().filter(email=emailcheck)
                namecheck = company_form.cleaned_data.get('name')
                nameexist = Profile.objects.all().filter(name=namecheck)
                if emailexist:
                    messages.error(request, "Ya se utilizo este E-Mail")
                elif nameexist:
                    messages.error(request, "Ya existe una empresa con ese nombre")
                else:
                    user = form.save()
                    user.profile.Department = company_form.cleaned_data['Department']
                    user.profile.location = company_form.cleaned_data['location']
                    user.profile.phone = company_form.cleaned_data['phone']
                    user.profile.name = company_form.cleaned_data['name']
                    user.profile.website = company_form.cleaned_data['website']
                    user.profile.instagram = company_form.cleaned_data['instagram']
                    user.profile.facebook = company_form.cleaned_data['facebook']
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
                usercheck = request.POST.get('username')
                userexist = User.objects.filter(username=usercheck)
                if userexist:
                    messages.error(request, "Ya se utilizo este Usuario")
                if form.cleaned_data.get('password1') != form.cleaned_data.get('password2'):
                    messages.error(request, "Las contraseñas son diferentes")
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
        order = Order.objects.all().filter(user=request.user.id, status='NoPagados')
    else:
        order = ''
    
    pcorder = Order.objects.all().filter(user=request.user.id, status='Procesando')
    if pcorder:
        porder = Order.objects.all().filter(user=request.user.id, status='Procesando')
    else:
        porder = ''
    
    ecorder = Order.objects.all().filter(user=request.user.id, status='Enviado')
    if ecorder:
        eorder = Order.objects.all().filter(user=request.user.id, status='Enviado')
    else:
        eorder = ''
    
    pacorder = Order.objects.all().filter(user=request.user.id, status='Pagado')
    if pacorder:
        pagorder = Order.objects.all().filter(user=request.user.id, status='Pagado')
    else:
        pagorder = ''
    
    cocorder = Order.objects.all().filter(user=request.user.id, status='Comentado')
    if cocorder:
        comeorder = Order.objects.all().filter(user=request.user.id, status='Comentado')
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
