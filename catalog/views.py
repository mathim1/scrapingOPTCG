from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProductoSerializer
from .models import Producto, Card
from decimal import Decimal
import requests
import math
from django.http import HttpResponse

def hello_world(request):
    return HttpResponse("Hello World")

def obtener_tasas_cambio():
    url = "https://openexchangerates.org/api/latest.json?app_id=132beca8844b465cb190e92dbec85ef6"
    response = requests.get(url)
    tasas_cambio = {'USD': Decimal('1'), 'CLP': Decimal('1'), 'JPY': Decimal('1')}
    if response.status_code == 200:
        data = response.json()
        tasas_cambio['USD'] = data['rates']['CLP']  # USD a CLP
        tasas_cambio['JPY'] = data['rates']['CLP'] / data['rates']['JPY']  # JPY a CLP
    else:
        pass
    return tasas_cambio


def format_clp(value):
    return "{:,.0f}".format(value).replace(",", ".")


class CatalogoView(APIView):
    def get(self, request, format=None):
        moneda_filtro = request.query_params.get('moneda')
        productos = Producto.objects.filter(precio__gt=0).select_related('moneda')

        if moneda_filtro:
            if moneda_filtro == 'CLP':
                productos = productos.filter(moneda__moneda='CLP')
            else:
                productos = productos.exclude(moneda__moneda='CLP')

        tasas_cambio = obtener_tasas_cambio()
        productos_precio_clp = {}

        for producto in productos:
            if producto.moneda.moneda != 'CLP':
                tasa_cambio = tasas_cambio.get(producto.moneda.moneda, Decimal('1'))
                tasa_cambio_decimal = Decimal(str(tasa_cambio))
                precio_clp_decimal = Decimal(str(producto.precio)) * tasa_cambio_decimal
                producto.precio_clp = math.ceil(precio_clp_decimal)
            else:
                producto.precio_clp = Decimal(str(producto.precio))

            productos_precio_clp.setdefault((producto.nombre, producto.idioma), []).append(producto)

        productos_menor_precio = []
        for key, group in productos_precio_clp.items():
            producto_menor_precio = min(group, key=lambda x: x.precio_clp)
            producto_menor_precio.precio_clp = format_clp(producto_menor_precio.precio_clp)
            productos_menor_precio.append(producto_menor_precio)

        serializer = ProductoSerializer(productos_menor_precio, many=True)
        return Response(serializer.data)


def obtener_precio(carta_id):
    try:
        carta = Card.objects.get(carid=carta_id)
        return carta.price
    except Card.DoesNotExist:
        return 0  # O manejar de otra manera si la carta no existe

