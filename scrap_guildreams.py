import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onePieceTCG.settings")

import django
django.setup()

from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from catalog.models import Producto, Moneda

s = HTMLSession()

def obtener_info_producto(url):
    def obtener_info_producto(url):
        print(f"Verificando URL: {url}")  # Impresión de diagnóstico
        if not url.startswith("https://www.guildreams.cl/"):
            print("URL no válida")  # Más impresiones de diagnóstico
            return None

    options = Options()
    options.headless = True  # Ejecutar en modo sin cabeza
    service = Service('C:/Windows/chromedriver-win64/chromedriver.exe')

    # Inicializar el WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Abrir la página
        driver.get(url)
        time.sleep(5)  # Esperar a que el JavaScript se ejecute

        # Obtener el HTML de la página y usar BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Resto del procesamiento de la página
        div_col_sm = soup.find('div', class_='col-sm')
        if not div_col_sm:
            return {'title': 'No se encontró la división', 'price': 0}

        product_title_element = div_col_sm.find('h2')
        product_title = product_title_element.text.strip() if product_title_element else 'No se encontró el título'

        final_price_element = div_col_sm.find('span', {'data-bs': 'product.finalPrice'})
        if final_price_element:
            final_price = final_price_element.text.strip()
            final_price = final_price.replace('$', '').replace(' ', '').replace('.', '')
        else:
            final_price = '0'

        total_price = int(final_price)

        return {'title': product_title, 'price': total_price}
    finally:
        driver.quit()

# Primero obtenemos el id de la moneda CLP
moneda_clp = Moneda.objects.get(moneda='CLP')

# Luego obtenemos todos los productos que tengan esa moneda
productos = Producto.objects.filter(moneda=moneda_clp)

# Iterar sobre los productos y actualizar la información en la base de datos
for producto in productos:
    # Solo procesar el producto si la URL base es la correcta
    if producto.url.startswith("https://www.guildreams.com/"):
        info_producto = obtener_info_producto(producto.url)
        if info_producto:
            # Imprimir la información obtenida
            print(f'Título para {producto.nombre}: {info_producto["title"]}')
            print(f'Precio Total para {producto.nombre}: {info_producto["price"]}')
            print('---')

            # Actualizar el campo de precio en la base de datos
            producto.precio = info_producto['price']
            producto.save()

