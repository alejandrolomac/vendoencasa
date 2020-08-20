from django.contrib import admin

from .models import Wish, WishItem

class WishAdmin(admin.ModelAdmin):
	list_display = (
        'id',
		'orderCode',
		'user',
        'ordered_date',
	)

	search_fields = ( 'orderCode', 'user', 'id', )
	list_filter = ( 'ordered_date', )

admin.site.register(WishItem)
admin.site.register(Wish, WishAdmin)