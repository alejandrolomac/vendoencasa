from django.urls import path
from . import views

app_name = "wish_app"

urlpatterns = [
    path('add-wish/<slug>', views.add_to_whis, name='add_to_whis'),
    path('wish-list/', views.WishSummaryView.as_view(), name='wish'),
] 