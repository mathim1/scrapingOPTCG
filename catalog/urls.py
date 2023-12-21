from django.urls import path
from .views import CatalogoView

urlpatterns = [
    # ... tus otras urls
    path('catalogo/', CatalogoView.as_view(), name='catalogo-api'),
]
