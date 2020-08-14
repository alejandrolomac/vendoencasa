from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "dashboard_app"

urlpatterns = [
	path('miempresa/', views.dashboard, name='dashboard'),
    path('miempresa/editar-producto/<product_id>', views.editproduct, name='editproduct'),
    path('miempresa/eliminar-producto/<pk>', views.deleteproduct, name='deleteproduct'),
    path('miempresa/productos', views.dashproduct, name='dashprod'),
    path('miempresa/nuevo-producto', views.dashnewprod, name='newprod'),
    path('miempresa/servicios', views.dashboardservices, name='dashserv'),
    path('miempresa/catalogo', views.dashcatalogue, name='dashcatalogue'),
    path('miempresa/nuevo-catalogo', views.dashnewcatalogue, name='newcatalogue'),
    path('miempresa/editar-catalogo/<product_id>', views.editcatalogue, name='editcatalogue'),
    path('miempresa/eliminar-catalogo/<pk>', views.deletecatalogue, name='deletecatalogue'),
    path('miempresa/cuenta', views.dashsetting, name='settings')
]