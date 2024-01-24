from django.urls import path
from .views import *

urlpatterns = [
    path('', CatalogoView.as_view(), name='catalogo-api'),
]
