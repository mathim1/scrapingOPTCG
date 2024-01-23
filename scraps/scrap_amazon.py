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
    r = s.get(url)
    soup = BeautifulSoup(r.html.html, 'html.parser')

    # Obtener el título
    product_title_element = soup.find('span', {'id': 'productTitle'})
    product_title = product_title_element.text.strip() if product_title_element else 'No se encontró el título'

    # Buscar directamente el texto del precio total
    total_text_element = soup.find(string='Total')
    price_text = total_text_element.find_next('span', {
        'class': 'a-size-base a-color-base'}).text.strip() if total_text_element else '0'

    # Extraer el valor numérico del precio eliminando el 'US$'
    price_value = float(price_text.replace('US$', '').replace(',', ''))

    return {'title': product_title, 'price': price_value}


def run_scraping_amazon():
    # Primero obtenemos el id de la moneda USD
    moneda_usd = Moneda.objects.get(moneda='USD')

    # Luego obtenemos todos los productos que tengan esa moneda
    productos = Producto.objects.filter(moneda=moneda_usd)

    # Iterar sobre los productos y actualizar la información en la base de datos
    for producto in productos:
        info_producto = obtener_info_producto(producto.url)

        # Imprimir la información obtenida
        print(f'Título para {producto.nombre}: {info_producto["title"]}')
        print(f'Precio Total para {producto.nombre}: {info_producto["price"]}')
        print('---')

        # Actualizar el campo de precio en la base de datos
        producto.precio = info_producto['price']
        producto.save()

run_scraping_amazon()