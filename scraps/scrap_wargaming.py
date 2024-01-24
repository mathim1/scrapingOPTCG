#!/home/ec2-user/onePieceTCG/env/bin/python3
import sys

sys.path.append('/home/ec2-user/onePieceTCG')

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onePieceTCG.settings")

import django

django.setup()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from catalog.models import Producto, Moneda
from selenium.common.exceptions import TimeoutException


def obtener_info_producto(url):
    if not url.startswith("https://www.wargaming.cl/"):
        return None

    options = Options()
    options.headless = True
    options.binary_location = '/home/ec2-user/chrome-headless-shell-linux64/chrome-headless-shell'  # Replace with actual path
    service = Service('/home/ec2-user/chromedriver-linux64/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)

        # Esperar a que el elemento esté presente
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.bs-product__title'))
            )
        except TimeoutException:
            print("Tiempo de espera agotado, no se encontró el título. Estableciendo el precio en 0.")
            return {'title': 'Tiempo de Espera Agotado', 'price': 0}

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Verificar si el producto está agotado
        stock_status_element = soup.find('p', {'class': 'lead'})
        if stock_status_element and "Producto presenta algunas dificultades" in stock_status_element.text:
            product_title_element = soup.find('h1', {'class': 'bs-product__title'})
            product_title = product_title_element.text.strip() if product_title_element else 'No se encontró el título'
            return {'title': product_title, 'price': 0}

        # Si el producto no está agotado, continúa con la obtención de la información
        product_title_element = soup.find('h1', {'class': 'bs-product__title'})
        product_title = product_title_element.text.strip() if product_title_element else 'No se encontró el título'

        final_price_element = soup.find('span', {'class': 'bs-product__final-price'})
        final_price = final_price_element.text.strip().replace('$', '').replace('.', '') if final_price_element else '0'

        total_price = int(final_price)

        return {'title': product_title, 'price': total_price}
    finally:
        driver.quit()


def run_scraping_wargaming():
    moneda_clp = Moneda.objects.get(moneda='CLP')
    productos = Producto.objects.filter(moneda=moneda_clp)

    for producto in productos:
        if producto.url.startswith("https://www.wargaming.cl/"):
            info_producto = obtener_info_producto(producto.url)
            if info_producto:
                print(f'Título para {producto.nombre}: {info_producto["title"]}')
                print(f'Precio Total para {producto.nombre}: {info_producto["price"]}')
                print('---')
                producto.precio = info_producto['price']
                producto.save()


run_scraping_wargaming()
