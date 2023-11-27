import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onePieceTCG.settings")

import django

django.setup()

from requests_html import HTMLSession
from catalog.models import Producto, Moneda
import requests

# Inicia la sesión HTTP
s = HTMLSession()

from bs4 import BeautifulSoup


def obtener_info_producto(url):
    if not url.startswith("https://www.gamingplace.cl/"):
        return None

    s = requests.Session()
    response = s.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Obtiene el título del producto
    product_title_element = soup.find('h1', {'class': 'page-header m-0 text-left'})
    product_title = product_title_element.text.strip() if product_title_element else 'No se encontró el título'

    # Verifica la disponibilidad del producto
    stock_element = soup.find('span', {'class': 'product-form-stock'})
    if stock_element and stock_element.text.strip().isdigit():
        stock = int(stock_element.text.strip())
        if stock <= 0:
            return {'title': product_title, 'price': 0}
    else:
        return {'title': product_title, 'price': 0}

    # Busca el precio
    final_price_element = soup.find('span', {'class': 'product-form-price form-price', 'id': 'product-form-price'})
    if final_price_element:
        final_price = final_price_element.text.strip().replace('$', '').replace(' CLP', '').replace('.', '')
    else:
        final_price = '0'

    total_price = int(final_price) if final_price.isdigit() else 'Precio no disponible'

    return {'title': product_title, 'price': total_price}


# Obtiene la instancia de la moneda CLP
moneda_clp = Moneda.objects.get(moneda='CLP')

# Obtener todos los productos con esa moneda
productos = Producto.objects.filter(moneda=moneda_clp)

# Iterar sobre los productos y actualizar la información en la base de datos
for producto in productos:
    # Procesar el producto si la URL base es correcta
    info_producto = obtener_info_producto(producto.url)
    if info_producto:
        # Imprimir la información obtenida
        print(f'Título para {producto.nombre}: {info_producto["title"]}')
        print(f'Precio Total para {producto.nombre}: {info_producto["price"]}')
        print('---')

        # Actualizar el campo de precio en la base de datos
        producto.precio = info_producto['price']
        producto.save()
