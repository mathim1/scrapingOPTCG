import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onePieceTCG.settings")

import django

django.setup()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from catalog.models import Producto, Moneda


def obtener_info_producto(url):
    if not url.startswith("https://www.magicsur.cl/"):
        return None

    options = Options()
    options.headless = True  # Ejecutar en modo sin cabeza
    service = Service('C:/Windows/chromedriver-win64/chromedriver.exe')

    with webdriver.Chrome(service=service, options=options) as driver:
        driver.get(url)
        time.sleep(5)  # Esperar a que el JavaScript se ejecute

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Verificar disponibilidad del producto
        disponibilidad_elemento = soup.find('span', {'id': 'product-availability'})
        if disponibilidad_elemento and "Fuera de stock" in disponibilidad_elemento.text:
            return {'title': 'Producto agotado', 'price': 0}

        # Obtener el título del producto desde el nuevo HTML
        product_title_element = soup.find('h1', {'class': 'h1 page-title'}).find('span')
        product_title = product_title_element.text.strip() if product_title_element else 'No se encontró el título'

        # Obtener el precio del producto
        price_element = soup.find('span', {'class': 'product-price current-price-value'})
        if price_element:
            final_price = price_element.text.strip().replace('$', '').replace('.', '').replace(' ', '')
        else:
            final_price = '0'

        total_price = int(final_price)

        return {'title': product_title, 'price': total_price}


# Obtiene la instancia de la moneda CLP
moneda_clp = Moneda.objects.get(moneda='CLP')

# Obtener todos los productos con esa moneda
productos = Producto.objects.filter(moneda=moneda_clp)

# Iterar sobre los productos y actualizar la información en la base de datos
for producto in productos:
    info_producto = obtener_info_producto(producto.url)
    if info_producto:
        print(f'Título para {producto.nombre}: {info_producto["title"]}')
        print(f'Precio Total para {producto.nombre}: {info_producto["price"]}')
        print('---')
        producto.precio = info_producto['price']
        producto.save()
