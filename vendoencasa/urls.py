from django.contrib import admin
from django.urls import path, re_path, include
urlpatterns = [
	re_path(r'', include('applications.product.urls')),
    re_path('admin/', admin.site.urls),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_ROOT}),
]
