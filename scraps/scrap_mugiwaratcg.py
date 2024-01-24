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
import requests

# Inicia la sesión HTTP
s = HTMLSession()


def obtener_info_producto(url):
    if not url.startswith("https://mugiwaratcg.com/"):
        return None

    response = s.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Verificar si el producto está agotado
    stock_status_button = soup.find('button', {'id': 'ProductSubmitButton-template--18477826146626__main'})
    if stock_status_button and 'Agotado' in stock_status_button.text:
        product_title_element = soup.find('h1')
        product_title = product_title_element.text.strip() if product_title_element else 'No se encontró el título'
        return {'title': product_title, 'price': 0}

    # Obtener el título del producto
    product_title_element = soup.find('h1')
    product_title = product_title_element.text.strip() if product_title_element else 'No se encontró el título'

    # Obtener el precio
    price_wrapper = soup.find('div', {'class': 'price__sale'})
    if price_wrapper:
        # Intenta encontrar un precio de oferta primero
        sale_price_element = price_wrapper.find('span', class_=lambda x: x and 'price-item--sale' in x.split())
        if sale_price_element:
            final_price = sale_price_element.text.strip().replace('$', '').replace('.', '').replace(' CLP', '')
        else:
            # Si no hay precio de oferta, busca el precio normal
            regular_price_element = price_wrapper.find('s', {'class': 'price-item price-item--regular'})
            final_price = regular_price_element.text.strip().replace('$', '').replace('.', '').replace(' CLP',
                                                                                                       '') if regular_price_element else '0'

    else:
        final_price = '0'

    total_price = int(final_price)

    return {'title': product_title, 'price': total_price}


def run_scraping_mugiwaratcg():
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

run_scraping_mugiwaratcg()