from rest_framework import serializers
from .models import *

class ProductoSerializer(serializers.ModelSerializer):
    precio_clp = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'type', 'idioma', 'image', 'moneda', 'precio_clp', 'url']

    def get_precio_clp(self, obj):
        return obj.precio_clp
