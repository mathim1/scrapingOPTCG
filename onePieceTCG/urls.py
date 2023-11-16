# onepiece_tcg/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls')),  # Incluye las URLs de la aplicación 'tienda'
]
