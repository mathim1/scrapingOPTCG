from django.shortcuts import render
from .models import Producto
from decimal import Decimal
from django.core.paginator import Paginator
import requests
import math


def catalogo(request):
    moneda_filtro = request.GET.get('moneda')

    productos = Producto.objects.filter(precio__gt=0).select_related('moneda')
    if moneda_filtro:
        if moneda_filtro == 'CLP':
            productos = productos.filter(moneda__moneda='CLP')
        else:
            productos = productos.exclude(moneda__moneda='CLP')

    tasas_cambio = obtener_tasas_cambio()

    # Crear un diccionario para almacenar los precios en CLP
    productos_precio_clp = {}

    for producto in productos:
        tasa_cambio = tasas_cambio.get(producto.moneda.moneda, Decimal('1'))
        tasa_cambio_decimal = Decimal(str(tasa_cambio))
        if producto.moneda.moneda == 'CLP':
            producto.precio_clp = producto.precio
        else:
            precio_clp_decimal = producto.precio * tasa_cambio_decimal
            producto.precio_clp = math.ceil(precio_clp_decimal)

        # Añadir el precio en CLP al producto para usarlo luego
        productos_precio_clp.setdefault((producto.nombre, producto.idioma), []).append(producto)

    # Encuentra el producto con el menor precio en CLP para cada grupo de nombre e idioma
    productos_menor_precio = []
    for key, group in productos_precio_clp.items():
        producto_menor_precio = min(group, key=lambda x: x.precio_clp)
        # Aplicar el formato a la propiedad de precio_clp para mostrarla correctamente
        producto_menor_precio.precio_clp = format_clp(producto_menor_precio.precio_clp)
        productos_menor_precio.append(producto_menor_precio)

    # Configurar la paginación
    paginator = Paginator(productos_menor_precio, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pasa el objeto de página al contexto del template
    return render(request, 'catalogo.html', {'page_obj': page_obj, 'moneda_filtro': moneda_filtro})


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
