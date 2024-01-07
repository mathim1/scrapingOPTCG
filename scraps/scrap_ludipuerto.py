import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onePieceTCG.settings")

import django

django.setup()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from catalog.models import Producto, Moneda
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def obtener_info_producto(url):
    if not url.startswith("https://www.ludipuerto.cl/"):
        return None

    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")  # Bypass OS security model, REQUIRED on Linux
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--disable-gpu")  # Applicable to windows os only
    options.add_argument("--disable-extensions")
    options.add_argument("--remote-debugging-port=9222")  # This is important

    service = Service('/usr/local/bin/chromedriver')

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Check if the product is out of stock
        stock_element = soup.find('p', {'class': 'stock out-of-stock'})
        if stock_element and stock_element.text.strip() == 'Agotado':
            return {'title': 'Producto Agotado', 'price': 0}

        # Extract the product title
        try:
            product_title_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.product_title.wd-entities-title'))
            )
            product_title = product_title_element.text.strip()
        except TimeoutException:
            print("Tiempo de espera agotado, no se encontró el título del producto.")
            return {'title': 'Tiempo de Espera Agotado', 'price': 0}

        # Extract the price
        price_element = soup.find('p', {'class': 'price'})
        final_price = '0'
        if price_element:
            final_price_element = price_element.find('span', {'class': 'amount'})
            if final_price_element:
                final_price = final_price_element.text.strip().replace('$', '').replace('.', '')

        total_price = int(final_price)
        return {'title': product_title, 'price': total_price}

    finally:
        driver.quit()


# Rest of your code
moneda_clp = Moneda.objects.get(moneda='CLP')
productos = Producto.objects.filter(moneda=moneda_clp)

for producto in productos:
    info_producto = obtener_info_producto(producto.url)
    if info_producto:
        print(f'Título para {producto.nombre}: {info_producto["title"]}')
        print(f'Precio Total para {producto.nombre}: {info_producto["price"]}')
        print('---')
        producto.precio = info_producto['price']
        producto.save()
