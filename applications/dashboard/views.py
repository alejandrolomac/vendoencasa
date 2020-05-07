from django.shortcuts import render, redirect
from applications.product.models import Company, Category, SubCategory, Products
from applications.services.models import Services
from django.db.models import Count
from django.contrib.auth.models import User
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required(login_url='useradmin_app:entrar')
def dashboard(request):
    companysCount = Company.objects.all().count()
    productsCount = Products.objects.all().count()
    servicesCount = Services.objects.all().count()
    usersCount = User.objects.all().count()
    showProducts = Products.objects.all()[:10]
    return render(request, 'dash-escritorio.html', {'CompanysCount': companysCount, 'ProductsCount': productsCount, 'UsersCount': usersCount, 'ServicesCount': servicesCount, 'ShowProduct': showProducts})

@login_required(login_url='useradmin_app:entrar')
def dashproduct(request):
    form = ProductForm(request.POST, request.FILES)
    if form.is_valid():
        formprod = form.save(commit=False)
        formprod.title = request.POST.get('title')
        print("TITULO: " + request.POST.get('title'))
        print("Precio: " + request.POST.get('price'))
        formprod.price = request.POST.get('price')
        formprod.imagef = request.FILES['imagef']
        formprod.save()
        form.save_m2m()
        return redirect("dashboard_app:dashprod")
    return render(request,'dash-prod.html', {'form':form})

@login_required(login_url='useradmin_app:entrar')
def dashboardservices(request):
	data = {}
	return render(request,'dash-services.html', data)