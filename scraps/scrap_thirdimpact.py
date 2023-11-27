import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onePieceTCG.settings")

import django

django.setup()

from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
from catalog.models import Producto, Moneda

s = HTMLSession()


def obtener_info_producto(url):
    print(f"Verificando URL: {url}")
    if not url.startswith("https://thirdimpact.cl/"):
        print("URL no válida")
        return None

    options = webdriver.ChromeOptions()
    options.headless = True
    service = Service('C:/Windows/chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        time.sleep(5)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Obtención del título del producto
        product_title_element = soup.find('h1', {'class': 'product-title product_title entry-title'})
        product_title = product_title_element.text.strip() if product_title_element else 'No se encontró el título'

        # Verificar si el producto está agotado
        stock_element = soup.find('p', {'class': 'stock out-of-stock'})
        if stock_element and stock_element.text.strip() == 'Agotado':
            print('Producto agotado')
            return {'title': product_title, 'price': 0}

        # Búsqueda de precio
        price_element = soup.find('p', {'class': 'price product-page-price price-on-sale'})
        final_price = None

        if price_element:
            # Prioridad al precio con descuento (dentro de <ins>)
            discounted_price = price_element.find('ins')
            if discounted_price:
                final_price = discounted_price.text.strip().replace('$', '').replace('.', '')
        else:
            # Buscar el precio normal en la etiqueta <p class="price product-page-price">
            price_element = soup.find('p', {'class': 'price product-page-price'})
            if price_element:
                normal_price = price_element.find('span', {'class': 'woocommerce-Price-amount amount'})
                if normal_price:
                    final_price = normal_price.text.strip().replace('$', '').replace('.', '')

        total_price = int(final_price) if final_price and final_price.isdigit() else 0

        return {'title': product_title, 'price': total_price}


    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return None
    finally:
        driver.quit()


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

