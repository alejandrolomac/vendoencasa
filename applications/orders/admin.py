from django.contrib import admin
from .models import OrdersProducts

class OrdersProductsAdmin(admin.ModelAdmin):
	list_display = (
		'id',
		'title',
		'subCategory',
		'company',
		'productCode',
	)

	search_fields = ( 'title', 'productCode', )
	list_filter = ( 'subCategory', 'season', 'virus', )

admin.site.register(OrdersProducts, OrdersProductsAdmin)