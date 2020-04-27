from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls import handler400, handler403, handler404 
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

handler404 = 'applications.product.views.handler404'
handler403 = 'applications.product.views.handler403'
handler400 = 'applications.product.views.handler400'

urlpatterns = [
    re_path('admin/', admin.site.urls),
	re_path('', include('applications.product.urls')),
    re_path('', include('applications.cart.urls')),
    re_path('', include('applications.useradmin.urls')),
    re_path('', include('applications.services.urls')),
    re_path('accounts/', include('allauth.urls')),
    re_path('login/', auth_views.LoginView.as_view(), name='login'),
    re_path('logout/', auth_views.LogoutView.as_view(next_page='logout')), 
    re_path('oauth/', include('social_django.urls', namespace='social')),
]
