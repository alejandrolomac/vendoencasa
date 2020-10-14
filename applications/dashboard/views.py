from django.shortcuts import render, redirect, get_object_or_404
from applications.product.models import Company, Category, SubCategory, Products, DiscountCode, RegistrationCode
from applications.services.models import Services
from applications.useradmin.models import Profile
from applications.cart.models import Order
from applications.orders.models import OrdersProducts
from django.db.models import Count
from django.contrib.auth.models import User
from .forms import ProductForm, OrdersForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import (
	TemplateView, 
	ListView,
)
from .forms import CreateCompanyForm, CompanyForm
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models import Avg
from django.db.models import Sum

@login_required(login_url='useradmin_app:entrar')
def dashboard(request):
    iduser = request.user.id
    companysCount = Company.objects.select_related().count()
    productsCount = Products.objects.select_related().filter(user__id=iduser).count()
    servicesCount = Services.objects.select_related().count()
    usersCount = User.objects.select_related().count()
    showProducts = Products.objects.select_related()[:10]

    viewsprod = Products.objects.select_related('user').filter(user__id=iduser).aggregate(Sum('views'))
    sellprod = Order.objects.select_related().filter(items__user__id=iduser, status='Pagado').count()
    sellprodlist = Order.objects.select_related().filter(items__user__id=iduser, status='Pagado')[:10]

    return render(request, 'dash-escritorio.html', {'CompanysCount': companysCount, 'ProductsCount': productsCount, 'UsersCount': usersCount, 'ServicesCount': servicesCount, 'ShowProduct': showProducts, 'viewsprod': viewsprod, 'sellprod': sellprod, 'sellprodlist': sellprodlist})


@login_required(login_url='useradmin_app:entrar')
def dashnewprod(request):
    iduser = request.user.id
    countprod = Products.objects.all().filter(user__id=iduser).count()
    userprofile = get_object_or_404(Profile, pk=request.user.profile.id)
    form = ProductForm(request.POST, request.FILES)
    if form.is_valid():
        formprod = form.save(commit=False)
        if formprod.pricePromo:
            formprod.imagef = request.FILES['imagef']
            formprod.user = request.user
            formprod.price = (( formprod.price * formprod.subCategory.category.commission ) / 100) + formprod.price
            formprod.available = True
            formprod.save()
            form.save_m2m()
            return redirect("dashboard_app:dashprod")
        else:
            formprod.imagef = request.FILES['imagef']
            formprod.user = request.user
            formprod.price = (( formprod.price * formprod.subCategory.category.commission ) / 100) + formprod.price
            formprod.available = True
            formprod.save()
            form.save_m2m()
            return redirect("dashboard_app:dashprod")

    return render(request,'dash-new-prod.html', {'form':form})


@login_required(login_url='useradmin_app:entrar')
def dashboardservices(request):
	data = {}
	return render(request,'dash-services.html', data)


@login_required(login_url='useradmin_app:entrar')
def editproduct(request, product_id):
    product_to_edit = get_object_or_404(Products, pk=product_id)
    fecha_pub = product_to_edit
    form = ProductForm(instance=product_to_edit)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product_to_edit)
        if form.is_valid():
            formprod = form.save(commit=False)
            if formprod.pricePromo:
                formprod.price = (( formprod.price * formprod.subCategory.category.commission ) / 100) + formprod.price
                formprod.save()
                form.save_m2m()
                return redirect("dashboard_app:dashprod")
            else:
                formprod.price = (( formprod.price * formprod.subCategory.category.commission ) / 100) + formprod.price
                formprod.save()
                form.save_m2m()
                return redirect("dashboard_app:dashprod")
        else:
            form = ProductForm(instance=product_to_edit)

    return render(request, "dash-edit-prod.html", {'form': form, 'product': product_to_edit, 'fechapub': fecha_pub})


@login_required(login_url='useradmin_app:entrar')
def deleteproduct(request, slug):
    product = get_object_or_404(Products, slug=slug)
    product.delete()
    return redirect('dashboard_app:dashprod')


@login_required(login_url='useradmin_app:entrar')
def dashproduct(request):
    iduser = request.user.id
    productlist = Products.objects.select_related('user').filter(user__id=iduser).order_by('-pub_date')
    countprod = Products.objects.select_related('user').filter(user__id=iduser).count()
    userprofile = get_object_or_404(Profile, pk=request.user.profile.id)
    paginator = Paginator(productlist, 9)

    page = request.GET.get('page')
    prodpage = paginator.get_page(page)

    context = {'productlist': prodpage, 'countprod': countprod, 'userprofile': userprofile, 'prodpage': prodpage}
    return render(request,'dash-prod.html', context)


@login_required(login_url='useradmin_app:entrar')
def dashsettingas(request):
    form = CreateCompanyForm(request.POST)
    company_form = CompanyForm(request.POST, request.FILES)
    context = {}
    return render(request,'dash-settings.html', context)


@login_required(login_url='useradmin_app:entrar')
def dashsetting(request):
    product_to_edit = get_object_or_404(User, pk=request.user.id)
    profile_to_edit = get_object_or_404(Profile, pk=request.user.profile.id)
    form = CreateCompanyForm(instance=product_to_edit)
    formp = CompanyForm(instance=profile_to_edit)
    if request.method == 'POST':
        form = CreateCompanyForm(request.POST, request.FILES, instance=product_to_edit)
        formp = CompanyForm(instance=profile_to_edit)
        if form.is_valid():
            form.save()
            formp.save()
            return redirect('dashboard_app:dashprod')
        else:
            form = CreateCompanyForm(instance=product_to_edit)
            formp = CompanyForm(instance=profile_to_edit)

    return render(request, "dash-settings.html", {'form': form, 'formp': formp, 'product': product_to_edit})


@login_required(login_url='useradmin_app:entrar')
def dashcatalogue(request):
    iduser = request.user.id
    productlist = OrdersProducts.objects.select_related('user').filter(user__id=iduser)
    countprod = OrdersProducts.objects.select_related('user').filter(user__id=iduser).count()
    userprofile = get_object_or_404(Profile, pk=request.user.profile.id)

    context = {'productlist': productlist, 'countprod': countprod, 'userprofile': userprofile}
    return render(request,'dash-catalogue.html', context)


@login_required(login_url='useradmin_app:entrar')
def dashnewcatalogue(request):
    iduser = request.user.id
    countprod = OrdersProducts.objects.all().filter(user__id=iduser).count()
    userprofile = get_object_or_404(Profile, pk=request.user.profile.id)
    form = OrdersForm(request.POST, request.FILES)
    if form.is_valid():
        formprod = form.save(commit=False)
        formprod.imagef = request.FILES['imagef']
        formprod.user = request.user
        formprod.available = True
        formprod.save()
        form.save_m2m()
        return redirect("dashboard_app:dashcatalogue")

        
    return render(request,'dash-new-catalogue.html', {'form':form})


@login_required(login_url='useradmin_app:entrar')
def editcatalogue(request, product_id):
    product_to_edit = get_object_or_404(OrdersProducts, pk=product_id)
    fecha_pub = product_to_edit
    form = ProductForm(instance=product_to_edit)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product_to_edit)
        if form.is_valid():
            form.save()
            return redirect('dashboard_app:dashcatalogue')
        else:
            form = ProductForm(instance=product_to_edit)

    return render(request, "dash-edit-catalogue.html", {'form': form, 'product': product_to_edit, 'fechapub': fecha_pub})


@login_required(login_url='useradmin_app:entrar')
def deletecatalogue(request, pk):
    product = get_object_or_404(OrdersProducts, pk=pk)
    product.delete()
    return redirect('dashboard_app:dashcatalogue')