#!/usr/bin/python3
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
    if not url.startswith("https://www.tiendalacomarca.cl/"):
        return None

    response = s.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Verificar si el producto está agotado mediante el código 404
    not_found_div = soup.find('div', {'class': 'home-title'})
    if not_found_div and '404' in not_found_div.text:
        return {'title': 'Producto no encontrado', 'price': 0}

    # Obtención del título del producto
    product_title_element = soup.find('h1', {'class': 'product-single__title'})
    product_title = product_title_element.text.strip() if product_title_element else 'No se encontró el título'

    # Obtención del precio del producto
    price_container = soup.find('div', {'class': 'price-product'})
    if price_container:
        # Intenta encontrar un precio de oferta primero
        discounted_price_element = price_container.find('s', {'class': 'product-price__price is-bold'})
        regular_price_element = price_container.find('span', {'itemprop': 'price'}, style="text-decoration: none;")

        # Determinar si usar el precio con descuento o el precio regular
        if discounted_price_element:
            final_price = discounted_price_element.text.strip().replace('$', '').replace('.', '').replace('CLP',
                                                                                                          '').strip()
        elif regular_price_element:
            final_price = regular_price_element.text.strip().replace('$', '').replace('.', '').replace('CLP',
                                                                                                       '').strip()
        else:
            final_price = '0'
    else:
        final_price = '0'

    # Check if final_price is an empty string and set it to '0' if it is
    if final_price == '':
        final_price = '0'

    total_price = int(final_price)

    return {'title': product_title, 'price': total_price}

def run_scraping_lacomarca():
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

run_scraping_lacomarca()