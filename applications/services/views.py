from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views.generic import (
	TemplateView, 
	ListView,
)
from .models import Services
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.db.models import Count

class listServices(ListView):
	template_name = 'services.html'
	paginate_by = 40
	model = Services
	context_object_name = 'services'

class SingleServices(ListView):
	template_name = "single-services.html"
	context_object_name = 'singleServices'

	def get_queryset(self):
		id = self.kwargs['slug']
		lista = Services.objects.all().filter(
			slug=id,
		)
		return lista