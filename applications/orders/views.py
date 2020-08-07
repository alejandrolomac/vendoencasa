from django.shortcuts import render, redirect
from django.views.generic import (
	TemplateView, 
	ListView,
	DetailView,
	View,
)
from .models import OrdersProducts
from applications.product.models import Category
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

def indexOrders(request):
	paginate_by = 18
	categorys = Category.objects.all().filter()
	productslist = OrdersProducts.objects.all().filter(available=True).order_by('-pub_date')
	paginator = Paginator(productslist, 18)

	page = request.GET.get('page')
	contacts = paginator.get_page(page)
	return render(request, 'orders-list.html', {'listCategorys': categorys, 'contacts': contacts})


class SingleOrders(ListView):
	template_name = "single-orders.html"
	context_object_name = 'singleOrder'

	def get_queryset(self):
		id = self.kwargs['slug']
		lista = OrdersProducts.objects.all().filter(
			slug=id, 
			available=True
		)
		return lista

	def get_context_data(self, **kwargs):
		id = self.kwargs['slug']
		context = super(SingleOrders, self).get_context_data(**kwargs)
		product_select = OrdersProducts.objects.get(slug=id)
		products_cats = OrdersProducts.objects.all().filter(subCategory=product_select.subCategory, available=True)[:10]
		context['related_prod'] = products_cats
		purchase_message = 'https://api.whatsapp.com/send?phone=50499394028&text='
		if self.request.user.is_authenticated:
			#name
			if self.request.user.first_name != '' and self.request.user.last_name != '':
				usuario_name = self.request.user.first_name
			elif self.request.user.first_name != '':
				usuario_name = self.request.user.first_name + " " + self.request.user.last_name
			else:
				usuario_name = self.request.user.username

			#location
			if self.request.user.profile.location != '':
				location = '%0D%0ADirección: ' + self.request.user.profile.location

			#product
			title_product = OrdersProducts.objects.get(slug=id).title
			price_total = OrdersProducts.objects.get(slug=id).total_price()
		else:
			usuario_name = ''
			location = ''
		
		final_message = str(purchase_message) + '--- Nuevo pedido de ' + str(usuario_name) + '---%0D%0A%0D%0A'+ str(title_product) + '%0D%0A' + "----- Pago total: " + str(price_total) + "L." + str(location)
		context['purchase_message'] = final_message
		return context