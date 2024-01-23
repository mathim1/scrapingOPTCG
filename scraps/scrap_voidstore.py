import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onePieceTCG.settings")

import django

django.setup()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from catalog.models import Producto, Moneda
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def obtener_info_producto(url):
    if not url.startswith("https://www.voidstore.cl/"):
        return None

    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")  # Bypass OS security model, REQUIRED on Linux
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--disable-gpu")  # Applicable to windows os only
    options.add_argument("--disable-extensions")
    options.add_argument("--remote-debugging-port=9222")  # This is important

    service = Service('/opt/bin/chromedriver')

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.container.my-5.pt-lg-0.pt-5.product-page')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Verificar la disponibilidad del producto
        stock_div = soup.find('div', id='stock')
        in_stock = False
        if stock_div:
            stock_span = stock_div.find('span', class_='product-form-stock')
            if stock_span and stock_span.text.isdigit():
                in_stock = True

        if not in_stock:
            return {'title': 'Producto sin stock', 'price': 0, 'in_stock': False}

        # Extracción del título del producto
        product_title_element = soup.find('h1', {'class': 'page-header m-0 text-left'})
        product_title = product_title_element.text.strip() if product_title_element else 'No se encontró el título'

        # Extracción del precio del producto
        price_wrapper = soup.find('div', {'class': 'form-price_desktop'})
        final_price = '0'
        if price_wrapper:
            final_price_element = price_wrapper.find('span', {'class': 'product-form-price form-price'})
            if final_price_element:
                final_price = final_price_element.text.strip().replace('$', '').replace('.', '')
        total_price = int(final_price)

        return {'title': product_title, 'price': total_price, 'in_stock': in_stock}

    finally:
        driver.quit()

def run_scraping_voidstore():
    # Obtiene la instancia de la moneda CLP
    moneda_clp = Moneda.objects.get(moneda='CLP')

    # Obtener todos los productos con esa moneda
    productos = Producto.objects.filter(moneda=moneda_clp)

    for producto in productos:
        info_producto = obtener_info_producto(producto.url)
        if info_producto:
            print(f'Título para {producto.nombre}: {info_producto["title"]}')
            print(f'Precio Total para {producto.nombre}: {info_producto["price"]}')
            print('---')
            producto.precio = info_producto['price']
            producto.save()
