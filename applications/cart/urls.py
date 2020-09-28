from django.urls import path
from . import views

app_name = "cart_app"

urlpatterns = [
    path('add/<slug>', views.add_to_cart, name='add-to-cart'),
    path('add-c/<slug>/<color>', views.add_to_cart_color, name='add-to-cart-color'),
    path('add-s/<slug>/<size>', views.add_to_cart_size, name='add-to-cart-size'),
    path('add-cs/<slug>/<color>/<size>', views.add_to_cart_color_size, name='add-to-cart-color-size'),
    path('add-from-wish/<slug>', views.add_to_cart_from_wish, name='add-to-cart-from-wish'),
    path('remove/<slug>', views.remove_from_cart, name='remove-to-cart'),
    path('remove-c/<slug>/<color>', views.remove_from_cart_c, name='remove-to-cart-color'),
    path('remove-sc/<slug>/<color>/<size>', views.remove_from_cart_sc, name='remove-to-cart-size-color'),
    path('remove-s/<slug>/<size>', views.remove_from_cart_s, name='remove-to-cart-size'),
    path('clean/', views.clean_cart, name='clean-cart'),
    path('order/', views.OrderSummaryView.as_view(), name='order'),
    path('order-pay/', views.OrderSummaryPay.as_view(), name='orderpay'),
    path('order-finish/', views.orderSummaryFinish, name='orderfinish'),
    path('order-send/', views.orderSummaryEnds, name='orderend'),
    path('vendo-admin-orders/', views.orderAdmin, name='orderadmin'),
    path('vendo-admin-orders/s/<pk>', views.sendOrder, name='sendorder'),
    path('vendo-admin-orders/c/<pk>', views.completeOrder, name='completeorder'),
    path('vendo-admin-orders/d/<pk>', views.cancelOrder, name='cancelorder'),
    path('vendo-admin-orders/w/<pk>', views.whatsappOrder, name='whatsapporder'),

    path('delete/<slug>', views.delete_item, name='delete-to-cart'),
    path('delete-c/<slug>/<color>', views.delete_item_c, name='delete-to-cart-color'),
    path('delete-s/<slug>/<size>', views.delete_item_s, name='delete-to-cart-size'),
    path('delete-sc/<slug>/<color>/<size>', views.delete_item_sc, name='delete-to-cart-size-color'),
] 