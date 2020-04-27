from django.contrib import admin
from .models import Services

class ServicesAdmin(admin.ModelAdmin):
	list_display = (
		'id',
		'name',
	)

	search_fields = ( 'name', )

admin.site.register(Services, ServicesAdmin)