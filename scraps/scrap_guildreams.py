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

s = HTMLSession()


def obtener_info_producto(url):
    if not url.startswith("https://www.guildreams.com/"):
        return None

    options = Options()
    options.headless = True
    service = Service('C:/Windows/chromedriver-win64/chromedriver.exe')

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-bs="product.stock"]'))
            )
        except TimeoutException:
            print("Tiempo de espera agotado, no se encontró el elemento. Estableciendo el precio en 0.")
            return {'title': 'Tiempo de Espera Agotado', 'price': 0}

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Verificar si el producto está agotado
        stock_info = soup.find('div', {'data-bs': 'product.stock'})
        if stock_info and "Agotado" in stock_info.text:
            return {'title': 'Producto Agotado', 'price': 0}

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


moneda_clp = Moneda.objects.get(moneda='CLP')
productos = Producto.objects.filter(moneda=moneda_clp)

for producto in productos:
    if producto.url.startswith("https://www.guildreams.com/"):
        info_producto = obtener_info_producto(producto.url)
        if info_producto:
            print(f'Título para {producto.nombre}: {info_producto["title"]}')
            print(f'Precio Total para {producto.nombre}: {info_producto["price"]}')
            print('---')
            producto.precio = info_producto['price']
            producto.save()
