import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onePieceTCG.settings")

import django

django.setup()

from requests_html import HTMLSession
from catalog.models import Producto, Moneda
import requests
from bs4 import BeautifulSoup

# Inicia la sesión HTTP
s = HTMLSession()


def obtener_info_producto(url):
    if not url.startswith("https://deckkingdom.cl/"):
        return None

    s = requests.Session()
    response = s.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Verificar si el producto está agotado
    stock_status_button = soup.find('button', {'class': 'product-form__submit'})
    if stock_status_button and 'Agotado' in stock_status_button.text:
        product_title_container = soup.find('div', {'class': 'product__title'})
        product_title = product_title_container.find(
            'h1').text.strip() if product_title_container else 'No se encontró el título'
        return {'title': product_title, 'price': 0}

    # Si el producto no está agotado, continúa con la obtención de la información
    product_title_container = soup.find('div', {'class': 'product__title'})
    product_title = product_title_container.find(
        'h1').text.strip() if product_title_container else 'No se encontró el título'

    price_container = soup.find('div', {'class': 'price__container'})
    if price_container:
        final_price_element = price_container.find('span', {'class': 'price-item--sale'})
        if not final_price_element:
            final_price_element = price_container.find('span', {'class': 'price-item--regular'})

        final_price = final_price_element.text.strip().replace('$', '').replace('.', '').replace('CLP',
                                                                                                 '').strip() if final_price_element else '0'
    else:
        final_price = '0'

    total_price = int(final_price) if final_price.isdigit() else 0

    return {'title': product_title, 'price': total_price}


def run_scraping_deckkingdom():
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
