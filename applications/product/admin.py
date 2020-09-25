from django.contrib import admin
from .models import Company, Category, SubCategory, Products, Color, Size, Comment, DiscountCode, RegistrationCode

class CommentAdmin(admin.ModelAdmin):
	list_display = (
		'product',
		'user',
		'pub_date',
		'comment',
	)
	
class ColorAdmin(admin.ModelAdmin):
	list_display = (
		'name',
		'color',
	)

class SizeAdmin(admin.ModelAdmin):
	list_display = (
		'name',
	)

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
		'commission',
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
		'productCode',
	)

	search_fields = ( 'title', 'productCode', )
	list_filter = ( 'subCategory', 'season', 'virus', )

class RegistrationCodeAdmin(admin.ModelAdmin):
	list_display = (
		'associated',
		'code',
	)

	search_fields = ( 'associated', 'code', )

class DiscountCodeAdmin(admin.ModelAdmin):
	list_display = (
		'associated',
		'code',
		'typediscount',
		'discount',
	)

	search_fields = ( 'associated', 'code', )


admin.site.register(RegistrationCode, RegistrationCodeAdmin)
admin.site.register(DiscountCode, DiscountCodeAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Comment, CommentAdmin)