from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "orders_app"

urlpatterns = [
	path('pedidos', views.indexOrders, name="index"),
	path('pedidos/<slug>', views.SingleOrders.as_view(), name="single-orders"),
] 