from django.shortcuts import render, redirect
from django.views.generic import (
	TemplateView, 
	ListView,
)
from .models import Company, Category, SubCategory, Products
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import get_template
from django.contrib.auth.models import User

def index(request):
	categorys = Category.objects.all()
	new_prod = Products.objects.all().order_by('-pub_date')[:10]
	promo_prod = Products.objects.all().filter(promotion=True).order_by('-pub_date')[:10]
	return render(request, 'home.html', {'listCategorys': categorys, 'newProd': new_prod, 'promoProd': promo_prod})


class ListSubCategorys(ListView):
	template_name = 'categorys.html'
	paginate_by = 20

	def get_queryset(self):
		id = self.kwargs['pk']
		object_list = SubCategory.objects.filter(category__id=id)
		return object_list
	
	def get_context_data(self, **kwargs):
		id = self.kwargs['pk']
		context = super(ListSubCategorys, self).get_context_data(**kwargs)
		cats_selected = Category.objects.get(id=id)
		products_cats = Products.objects.all().filter(subCategory_id__category_id__id=id)
		context['catSelect'] = cats_selected
		context['productsCatSelect'] = products_cats
		return context


class ListSubCatProducts(ListView):
	template_name = 'cat-products.html'
	paginate_by = 20

	def get_queryset(self):
		id = self.kwargs['pk']
		object_list = Products.objects.filter(subCategory__id=id)
		return object_list


class ListCompanyProducts(ListView):
	template_name = 'company.html'

	def get_queryset(self):
		id = self.kwargs['pk']
		object_list = Products.objects.filter(company__id=id)
		return object_list


def listproducts(request):
	paginate_by = 20
	categorys = Category.objects.all()
	productslist = Products.objects.all().order_by('-pub_date')
	paginator = Paginator(productslist, 20)

	page = request.GET.get('page')
	contacts = paginator.get_page(page)
	return render(request, 'products.html', {'listCategorys': categorys, 'contacts': contacts})


class SingleProduct(ListView):
	template_name = "single-product.html"
	context_object_name = 'singleProduct'

	def get_queryset(self):
		id = self.kwargs['slug']
		lista = Products.objects.filter(
			slug=id
		)
		return lista

	def get_context_data(self, **kwargs):
		id = self.kwargs['slug']
		context = super(SingleProduct, self).get_context_data(**kwargs)
		product_select = Products.objects.get(slug=id)
		products_cats = Products.objects.all().filter(subCategory=product_select.subCategory)[:10]
		context['related_prod'] = products_cats
		return context


def search(request):
	query = request.GET.get('search-field')
	cat_query = request.GET.get('search-category')
	queryset = (Q(text__icontains=query))

	if( cat_query == '' ):
		queryset = ( 
			Q(title__icontains=query) | Q(resume__icontains=query)
		)
		results = Products.objects.filter(queryset).distinct().order_by('-pub_date')
	else:
		queryset = (
			Q(title__icontains=query) | Q(resume__icontains=query)
		)
		results = Products.objects.filter(queryset).distinct().filter( subCategory__id=cat_query).order_by('-pub_date')
	
	paginator = Paginator(results, 20)
	page = request.GET.get('page', 1)
	contacts = paginator.get_page(page)
	return render(request, 'search.html', {'contacts': contacts, 'querytext': query, 'count': results, 'query_page': query, 'query_page_tag': cat_query})
	

def plan(request):
	companysCount = Company.objects.all().count()
	productsCount = Products.objects.all().count()
	usersCount = User.objects.all().count()
	return render(request, 'plan.html', {'CompanysCount': companysCount, 'ProductsCount': productsCount, 'UsersCount': usersCount})

def handler400(request, exception):
	data = {}
	return render(request,'400.html', data)

def handler403(request, exception):
	data = {}
	return render(request,'403.html', data)

def handler404(request, exception):
	data = {}
	return render(request,'404.html', data)