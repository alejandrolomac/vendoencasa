from django.urls import path, re_path
from . import views

app_name = "product_app"

urlpatterns = [
	path('', views.Index.as_view(), name="index"),
	path('productos', views.ListProducts.as_view(), name="list-products"),
	path('Producto/<slug>', views.SingleProduct.as_view(), name="single-product"),
]