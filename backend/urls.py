from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'Parallel REST'
admin.site.site_title = 'Parallel REST'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('REST.urls')),
]
