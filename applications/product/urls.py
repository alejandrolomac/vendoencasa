from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "product_app"

urlpatterns = [
	path('', views.index, name="index"),
	path('productos', views.listproducts, name="list-products"),
	path('menos100', views.lessProduct, name="less-products"),
	path('producto/<slug>', views.SingleProduct.as_view(), name="single-product"),
	path('sub-categoria/<slug>/<pk>', views.ListSubCategorys.as_view(), name="sub-categorys"),
	path('productos/<slug>/<pk>/', views.ListSubCatProducts.as_view(), name="sub-catproducts"),
	path('empresa/<slug>/<pk>/', views.ListCompanyProducts.as_view(), name="company-products"),
	path('search/', views.search, name='search'),
	path('planes/', views.plan, name='planes')
] 