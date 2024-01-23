import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onePieceTCG.settings")

import django

django.setup()

from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from catalog.models import Producto, Moneda
from selenium.common.exceptions import TimeoutException
import re

# Inicia la sesión HTTP
s = HTMLSession()


def obtener_info_producto(url):
    # Check if the URL is from the desired domain
    if not url.startswith("https://www.gameofmagictienda.cl/"):
        return None

    # Selenium driver configuration
    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--remote-debugging-port=9222")

    service = Service('/opt/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Open the URL with Selenium
        driver.get(url)

        # Wait for the necessary elements to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.display-4, h1.bs-product__title"))
        )

        # Get the page source and parse it with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find the product title
        product_title_element = soup.find('h1', {'class': 'display-4'}) or soup.find('h1',
                                                                                     {'class': 'bs-product__title'})
        product_title = product_title_element.text.strip() if product_title_element else 'No se encontró el título'

        # Find the product price
        price_wrapper = soup.find('span', {'class': 'bs-product__final-price'})
        if price_wrapper:
            price_text = price_wrapper.text.strip()
            # Use regular expression to find all digits in the string
            digits = re.findall(r'\d+', price_text)
            final_price = ''.join(digits)
        else:
            final_price = '0'

        total_price = int(final_price)

        return {'title': product_title, 'price': total_price}

    except TimeoutException:
        return {'title': 'No se encontró el título', 'price': 0}

    finally:
        driver.quit()


def run_scraping_gameofmagic():
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
