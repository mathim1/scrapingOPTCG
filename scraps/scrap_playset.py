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
    # Verificar que la URL comience con "https://www.playset.cl/"
    if not url.startswith("https://www.playset.cl/"):
        return None

    # Realizar la solicitud HTTP al sitio web
    response = s.get(url)

    # Utilizar BeautifulSoup para parsear el HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    stock_status_element = soup.find('p', {'class': 'stock out-of-stock'})
    if stock_status_element and stock_status_element.text.strip() == "Sin existencias":
        # Producto sin stock
        return {'title': 'Producto sin stock', 'price': 0}

    # Obtener el título del producto del elemento H1 con la clase específica
    product_title_element = soup.find('h1', {'class': 'product-title product_title entry-title'})
    product_title = product_title_element.text.strip() if product_title_element else 'No se encontró el título'

    # Encontrar el precio final en el párrafo con la clase específica
    final_price_element = soup.find('p', {'class': 'price product-page-price'}).find('span', {
        'class': 'woocommerce-Price-amount amount'})
    final_price = final_price_element.text.strip().replace('$', '').replace('.', '') if final_price_element else '0'

    # Convertir el precio a un entero
    total_price = int(final_price)

    return {'title': product_title, 'price': total_price}


def run_scraping_playset():
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

run_scraping_playset()