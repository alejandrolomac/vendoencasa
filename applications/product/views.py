from django.shortcuts import render, redirect
from django.views.generic import (
	TemplateView, 
	ListView,
)
from .models import Company, Category, SubCategory, Products
from django.db.models import Q

class Index(ListView):
	template_name = 'home.html'
	model = Category
	context_object_name = 'listCategorys'


class ListSubCategorys(ListView):
	template_name = 'categorys.html'

	def get_queryset(self):
		id = self.kwargs['pk']
		object_list = SubCategory.objects.filter(category__id=id)
		return object_list


class ListSubCatProducts(ListView):
	template_name = 'cat-products.html'

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


class ListProducts(ListView):
	template_name = 'products.html'
	model = Products
	context_object_name = 'listProducts'
	paginate_by = 4


class ListCompanys(ListView):
	template_name = 'companys.html'
	model = Company
	context_object_name = 'listCompanys'
	paginate_by = 4


class SingleProduct(ListView):
	template_name = "single-product.html"
	context_object_name = 'singleProduct'

	def get_queryset(self):
		id = self.kwargs['slug']
		lista = Products.objects.filter(
			slug=id
		)
		return lista


class SearchResults(ListView):
	model = Products
	template_name = 'search.html'
	paginate_by = 4

	def get_queryset(self):
		query = self.request.GET.get('search-field')
		cat_query = self.request.GET.get('search-category')

		if( cat_query == '' ):
			object_list = Products.objects.filter(
		    	Q(title__icontains=query) | Q(resume__icontains=query)
		    )
		else:
			object_list = Products.objects.filter(
		    	Q(title__icontains=query) | Q(resume__icontains=query)
		    ).filter( subCategory__id=cat_query )

		return object_list