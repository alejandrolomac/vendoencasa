from django.shortcuts import render, redirect, get_object_or_404
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
def dashnewprod(request):
    form = ProductForm(request.POST, request.FILES)
    if form.is_valid():
        formprod = form.save(commit=False)
        formprod.imagef = request.FILES['imagef']
        formprod.save()
        form.save_m2m()
        return redirect("dashboard_app:dashprod")
    return render(request,'dash-new-prod.html', {'form':form})


@login_required(login_url='useradmin_app:entrar')
def dashproduct(request):
    productlist = Products.objects.all()
    countprod = Products.objects.all().count()
    context = {'productlist': productlist, 'countprod': countprod}
    return render(request,'dash-prod.html', context)


@login_required(login_url='useradmin_app:entrar')
def dashboardservices(request):
	data = {}
	return render(request,'dash-services.html', data)


@login_required(login_url='useradmin_app:entrar')
def editproduct(request, product_id):
    product_to_edit = get_object_or_404(Products, pk=product_id)
    form = ProductForm(instance=product_to_edit)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product_to_edit)
        if form.is_valid():
            form.save()
            return redirect('dashboard_app:dashprod')
        else:
            form = ProductForm(instance=product_to_edit)

    return render(request, "dash-edit-prod.html", {'form': form, 'product': product_to_edit})


@login_required(login_url='useradmin_app:entrar')
def deleteproduct(request, pk):
    product = get_object_or_404(Products, pk=pk)
    product.delete()
    return redirect('dashboard_app:dashprod')


@login_required(login_url='useradmin_app:entrar')
def dashsetting(request):
    context = {}
    return render(request,'dash-settings.html', context)