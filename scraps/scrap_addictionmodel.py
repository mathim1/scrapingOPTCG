#!/home/ec2-user/onePieceTCG/env/bin/python3
import sys

sys.path.append('/home/ec2-user/onePieceTCG')

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onePieceTCG.settings")

import django

django.setup()

from requests_html import HTMLSession
from catalog.models import Producto, Moneda
from bs4 import BeautifulSoup
import requests as s

# Inicia la sesión HTTP
s = HTMLSession()


def obtener_info_producto(url):
    # Verificar si la URL pertenece al dominio correcto
    if not url.startswith("https://addictionmodel.cl/"):
        return None

    response = s.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Verificar si el producto está agotado utilizando el botón "Sin stock"
    stock_button = soup.find('input', {
        'type': 'submit',
        'class': lambda x: x and 'product-buy-btn' in x.split(),
        'value': 'Sin stock'
    })

    if stock_button and stock_button.has_attr('disabled'):
        return {'title': 'Producto agotado', 'price': 0}

    # Obtener el título del producto
    product_title_element = soup.find('h1', {'id': 'product-name', 'itemprop': 'name'})
    product_title = product_title_element.text.strip() if product_title_element else 'No se encontró el título'

    # Obtener el precio del producto
    price_element = soup.find('span', {'class': 'price product-price js-price-display', 'id': 'price_display'})
    if price_element:
        final_price = price_element.text.strip().replace('$', '').replace('.', '')
        if final_price:
            total_price = int(final_price)
        else:
            total_price = 0
    else:
        total_price = 0

    return {'title': product_title, 'price': total_price}


def run_scraping_addictionmodel():
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


run_scraping_addictionmodel()
