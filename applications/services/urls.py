from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "services_app"

urlpatterns = [
	path('servicios', views.listServices.as_view(), name="list-services"),
	path('Servicio/<slug>', views.SingleServices.as_view(), name="single-services"),
] 