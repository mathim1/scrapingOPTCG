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
    if not url.startswith("https://www.lafortalezapuq.cl/"):
        return None

    response = s.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Verificar si el producto tiene stock
    out_of_stock_div = soup.find('div', {'id': 'out-of-stock'})
    in_stock = 'none' in out_of_stock_div.get('style', '').lower() if out_of_stock_div else False

    # Obtener el título del producto
    product_title_element = soup.find('h1')
    product_title = product_title_element.text.strip() if product_title_element else 'No se encontró el título'

    # Si el producto está fuera de stock, devolver precio 0
    if not in_stock:
        return {'title': product_title, 'price': 0, 'in_stock': in_stock}

    # Obtener el precio (solo si el producto está en stock)
    price_element = soup.find('span', {'id': 'product-price', 'class': 'price product-price'})
    if price_element:
        final_price = price_element.text.strip().replace('$', '').replace('.', '').replace(' CLP', '')
    else:
        final_price = '0'

    total_price = int(final_price) if final_price.isdigit() else 0

    return {'title': product_title, 'price': total_price, 'in_stock': in_stock}

def run_scraping_lafortaleza():
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
