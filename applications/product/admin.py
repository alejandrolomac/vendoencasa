from django.contrib import admin
from .models import Company, Category, SubCategory, Products

class CompanyAdmin(admin.ModelAdmin):
	list_display = (
		'id',
		'name',
	)

	search_fields = ( 'name', )

class CategoryAdmin(admin.ModelAdmin):
	list_display = (
		'id',
		'name',
	)

class SubCategoryAdmin(admin.ModelAdmin):
	list_display = (
		'id',
		'name',
	)

	list_filter = ( 'category', )

class ProductsAdmin(admin.ModelAdmin):
	list_display = (
		'id',
		'title',
		'subCategory',
		'company',
	)

	search_fields = ( 'title', )
	list_filter = ( 'subCategory', )

admin.site.register(Company, CompanyAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Products, ProductsAdmin)