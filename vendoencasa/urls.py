from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls import handler400, handler403, handler404 
from django.views.generic import TemplateView

handler404 = 'applications.product.views.handler404'
handler403 = 'applications.product.views.handler403'
handler400 = 'applications.product.views.handler400'

urlpatterns = [
	re_path('', include('applications.product.urls')),
    re_path('admin/', admin.site.urls),
    re_path('accounts/', include('allauth.urls')),
    re_path('', include('applications.cart.urls')),
    re_path('oauth/', include('social_django.urls', namespace='social')),
]
