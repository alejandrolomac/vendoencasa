from django.shortcuts import render
from django.views.generic import (
	ListView,
)
from .models import Company, Category, SubCategory, Products

class Index(ListView):
	template_name = 'index.html'
	model = Products
	context_object_name = 'productos'