from django.contrib import admin
from django.urls import path, include
from catalog.api import api as ninja_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/drf/', include('catalog.urls')),   # DRF pindah ke sini
    path('api/', ninja_api.urls),                # Ninja jadi /api/courses/
]