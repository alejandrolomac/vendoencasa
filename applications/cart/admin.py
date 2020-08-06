from django.contrib import admin

from .models import Order, OrderItem

class OrderAdmin(admin.ModelAdmin):
	list_display = (
        'id',
		'orderCode',
		'user',
        'ordered_date',
	)

	search_fields = ( 'orderCode', 'user', 'id', )
	list_filter = ( 'ordered_date', )

admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)