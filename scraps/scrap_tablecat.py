#!/home/ec2-user/onePieceTCG/env/bin/python3
import sys

sys.path.append('/home/ec2-user/onePieceTCG')

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onePieceTCG.settings")

import django

django.setup()

from requests_html import HTMLSession
from bs4 import BeautifulSoup
from catalog.models import Producto, Moneda

# Inicia la sesión HTTP
s = HTMLSession()


def obtener_info_producto(url):
    if not url.startswith("https://tablecatgames.cl/"):
        return None

    response = s.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    product_title_element = soup.find('h1', {'class': 'product_title entry-title'})
    product_title = product_title_element.text.strip() if product_title_element else 'No se encontró el título'

    # Encuentra el elemento del precio
    price_element = soup.find('p', {'class': 'price'})

    if price_element:
        final_price_element = price_element.find('span', {'class': 'woocommerce-Price-amount amount'})

        if final_price_element:
            final_price = final_price_element.text.strip().replace('$', '').replace('.', '')
        else:
            final_price = '0'
    else:
        final_price = '0'

    total_price = int(final_price)

    return {'title': product_title, 'price': total_price}


def run_scraping_tablecat():
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

run_scraping_tablecat()