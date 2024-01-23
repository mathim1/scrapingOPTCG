from django.urls import path
from .views import *

urlpatterns = [
    path('', CatalogoView.as_view(), name='catalogo-api'),
    path('run-all-scrapers/', RunAllScrapersView.as_view(), name='run-all-scrapers'),
]
