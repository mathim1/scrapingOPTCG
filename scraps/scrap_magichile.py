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

s = HTMLSession()


def obtener_info_producto(url):
    if not url.startswith("https://magic-chile.cl/"):
        return None

    s = HTMLSession()
    response = s.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Check for 'visible' in the class attribute to determine stock status
    unavailable_element = soup.find('div', class_=lambda x: x and 'product-unavailable' in x and 'visible' in x)
    out_of_stock_element = soup.find('div', class_=lambda x: x and 'product-out-stock' in x and 'visible' in x)

    # Determine if the product is available, out of stock, or unavailable
    if unavailable_element is not None:
        stock_status = 'No Disponible'
    elif out_of_stock_element is not None:
        stock_status = 'Agotado'
    else:
        stock_status = 'Disponible'

    # If the product is not available, return the stock status without fetching title or price
    if stock_status != 'Disponible':
        return {'title': 'No se encontró el título', 'price': 0, 'stock_status': stock_status}

    # Extracting product title
    title_element = soup.find('h1', class_='page-header m-0 text-left')
    product_title = title_element.text.strip() if title_element else 'No se encontró el título'

    # Extracting product price
    price_element = soup.find('span', class_='product-form-price form-price')
    if price_element:
        product_price = price_element.text.strip().replace('$', '').replace('.', '')
        product_price = int(product_price)
    else:
        product_price = 0

    return {'title': product_title, 'price': product_price, 'stock_status': stock_status}

def run_scraping_magichile():
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

run_scraping_magichile()