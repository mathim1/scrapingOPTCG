# tienda/urls.py
from django.urls import path
from .views import catalogo

urlpatterns = [
    path('catalogo/', catalogo, name='catalogo'),
    # Puedes agregar más patrones de URL según tus necesidades
]
