from django.contrib import admin

from .models import Order, OrderItem

class OrderAdmin(admin.ModelAdmin):
	list_display = (
        'id',
		'orderCode',
		'user',
		'status',
        'ordered_date',
	)

	search_fields = ( 'orderCode', 'user', 'id', )
	list_filter = ( 'ordered_date', 'status')

admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)