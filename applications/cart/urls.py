from django.urls import path
from . import views

app_name = "cart_app"

urlpatterns = [
    path('add/<slug>', views.add_to_cart, name='add-to-cart'),
    path('remove/<slug>', views.remove_from_cart, name='remove-to-cart'),
    path('order/', views.OrderSummaryView.as_view(), name='order'),
    path('remove-item/<slug>/', views.remove_single_item_from_cart,
         name='remove-item-cart'),
] 