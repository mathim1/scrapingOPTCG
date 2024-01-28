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
    if not url.startswith("https://www.malditomanga.cl/"):
        return None

    response = s.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    stock_status_element = soup.find('div', lambda
        class_: class_ and 'product-stock' in class_ and 'product-available' in class_ and 'visible' in class_)
    if not stock_status_element:
        # Si no tiene stock, regresar título con precio 0
        product_title_element = soup.find('h1', {'class': 'page-header m-0 text-left'})
        product_title = product_title_element.text.strip() if product_title_element else 'No se encontró el título'
        return {'title': product_title, 'price': 0}

    # Si el producto no está agotado, continúa con la obtención de la información
    product_title_element = soup.find('h1', {'class': 'page-header m-0 text-left'})
    product_title = product_title_element.text.strip() if product_title_element else 'No se encontró el título'

    price_element = soup.find('span', {'class': 'product-form-price form-price'})
    final_price = price_element.text.strip().split(' ')[0].replace('$', '').replace('.', '') if price_element else '0'
    total_price = int(final_price) if final_price.isdigit() else 0

    return {'title': product_title, 'price': total_price}


def run_scraping_mmanga():
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


run_scraping_mmanga()
