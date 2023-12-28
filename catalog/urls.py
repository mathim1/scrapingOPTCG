from django.urls import path
from .views import *

urlpatterns = [
    path('', hello_world, name='home'),
    path('catalogo/', CatalogoView.as_view(), name='catalogo-api'),
]
