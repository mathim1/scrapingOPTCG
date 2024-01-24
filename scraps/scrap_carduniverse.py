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

s = HTMLSession()


def obtener_info_producto(url):
    # Validar que la URL comience con 'https://carduniverse.cl/'
    if not url.startswith("https://carduniverse.cl/"):
        return None

    # Realizar la solicitud HTTP al sitio web
    response = s.get(url)

    # Utilizar BeautifulSoup para parsear el HTML
    soup = BeautifulSoup(response.html.html, 'html.parser')

    # Verificar si el producto está fuera de inventario o agotado
    out_of_stock_element = soup.find('div', {'class': 'product-block'})
    sold_out_element = soup.find('span', {'id': 'addToCartText-template--16843225235688__main'})

    if (out_of_stock_element and "Lo sentimos, este artículo está fuera de inventario" in out_of_stock_element.text) \
            or (sold_out_element and "Agotado" in sold_out_element.text):
        # Producto fuera de inventario o agotado
        return {'title': 'Producto no disponible', 'price': 0}

    # Obtener el título del producto
    product_title_element = soup.find('h1', {'class': 'page-title'})
    product_title = product_title_element.text.strip() if product_title_element else 'No se encontró el título'

    # Encontrar el precio del producto
    price_element = soup.find('form', {'id': 'product-form-template--16843225235688__main'})
    if price_element:
        final_price_element = price_element.find('span', {'class': 'money'})
        final_price = final_price_element.text.strip().replace('$', '').replace('.', '') if final_price_element else '0'
    else:
        final_price = '0'

    # Convertir el precio a un entero
    total_price = int(final_price)

    return {'title': product_title, 'price': total_price}


def run_scraping_carduniverse():
    # Obtener el ID de la moneda CLP
    moneda_clp = Moneda.objects.get(moneda='CLP')

    # Obtener todos los productos con esa moneda
    productos = Producto.objects.filter(moneda=moneda_clp)

    # Iterar sobre los productos y actualizar la información en la base de datos
    for producto in productos:
        info_producto = obtener_info_producto(producto.url)
        if info_producto:
            # Imprimir la información obtenida
            print(f'Título para {producto.nombre}: {info_producto["title"]}')
            print(f'Precio Total para {producto.nombre}: {info_producto["price"]}')
            print('---')

            # Actualizar el campo de precio en la base de datos
            producto.precio = info_producto['price']
            producto.save()

run_scraping_carduniverse()