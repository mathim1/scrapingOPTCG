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
    if not url.startswith("https://www.top8.cl/"):
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

        try:
            # Wait for the product title to appear
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.bs-product__title'))
            )
        except TimeoutException:
            print("Product title not found, setting price to 0")
            return {'title': 'Título no encontrado', 'price': 0}

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Obtener el título del producto
        product_title_element = soup.find('h1', {'class': 'bs-product__title'})
        product_title = product_title_element.text.strip() if product_title_element else 'No se encontró el título'

        # Verificar si el producto está agotado
        stock_status_element = soup.find('button', {'class': 'btn btn-danger w-100'})
        if stock_status_element and stock_status_element.text.strip() == 'Encargar':
            return {'title': product_title, 'price': 0}

        # Búsqueda del precio
        price_wrapper = soup.find('span', {'class': 'bs-product__final-price'})
        final_price = None

        if price_wrapper:
            final_price = price_wrapper.text.strip().replace('$', '').replace('.', '').replace('Ahora', '').strip()
        else:
            final_price = '0'

        total_price = int(final_price) if final_price.isdigit() else 0

        return {'title': product_title, 'price': total_price}

    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return None
    finally:
        driver.quit()

# Obtener la instancia de la moneda CLP
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
