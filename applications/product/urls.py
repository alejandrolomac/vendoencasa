from django.urls import path, re_path
from . import views

app_name = "product_app"

urlpatterns = [
	path('', views.Index.as_view(), name="index"),
]