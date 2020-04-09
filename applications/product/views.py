from django.shortcuts import render
from django.views.generic import (
	TemplateView, 
	ListView,
)
from .models import Company, Category, SubCategory, Products

class Index(TemplateView):
	template_name = 'home.html'


class ListProducts(ListView):
	template_name = 'products.html'
	model = Products
	context_object_name = 'listProducts'


class SingleProduct(ListView):
	template_name = "single-product.html"
	context_object_name = 'singleProduct'

	def get_queryset(self):
		id = self.kwargs['slug']
		lista = Products.objects.filter(
			slug=id
		)
		return lista