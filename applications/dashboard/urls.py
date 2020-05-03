from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "dashboard_app"

urlpatterns = [
	path('miempresa/', views.dashboard, name='dashboard'),
    path('miempresa/productos', views.dashproduct, name='dashprod'),
    path('miempresa/servicios', views.dashboardservices, name='dashserv')
]