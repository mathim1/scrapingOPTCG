import sys

sys.path.append('/home/ec2-user/onePieceTCG')

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onePieceTCG.settings")

import django

django.setup()

from requests_html import HTMLSession
from bs4 import BeautifulSoup
from catalog.models import Producto, Moneda

s = HTMLSession()


def obtener_info_producto(url):
    # Verificar que la URL comience con "https://www.geekers.cl/"
    if not url.startswith("https://www.geekers.cl/"):
        return None

    # Usar la sesión para manejar la solicitud
    r = s.get(url)
    # Parsear el HTML renderizado
    soup = BeautifulSoup(r.html.html, 'html.parser')

    # Verificar si el producto está agotado
    agotado_element = soup.find('h2', {'class': 'product-form__availability-title'})
    if agotado_element and agotado_element.text.strip() == "Agotado":
        return {'title': 'Producto Agotado', 'price': 0}

    # Obtener el título y precio del producto
    product_title_element = soup.find('h1', {'class': 'product-info__name'})
    product_title = product_title_element.text.strip() if product_title_element else 'No se encontró el título'

    final_price_element = soup.find('span', {'class': 'product-info__price-current'})
    final_price = final_price_element.text.strip().replace('$', '').replace('.', '') if final_price_element else '0'

    total_price = int(final_price)

    return {'title': product_title, 'price': total_price}

def run_scraping_geekers():
    moneda_clp = Moneda.objects.get(moneda='CLP')

    # Obtener todos los productos con esa moneda
    productos = Producto.objects.filter(moneda=moneda_clp)

    # Iterar sobre los productos y actualizar la información en la base de datos
    for producto in productos:
        # Solo procesar el producto si la URL base es la correcta
        info_producto = obtener_info_producto(producto.url)
        if info_producto:
            # Imprimir la información obtenida
            print(f'Título para {producto.nombre}: {info_producto["title"]}')
            print(f'Precio Total para {producto.nombre}: {info_producto["price"]}')
            print('---')

            # Actualizar el campo de precio en la base de datos
            producto.precio = info_producto['price']
            producto.save()

run_scraping_geekers()