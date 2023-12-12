import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onePieceTCG.settings")

import django

django.setup()

from requests_html import HTMLSession
from bs4 import BeautifulSoup
from catalog.models import Producto, Moneda

# Inicia la sesión HTTP
s = HTMLSession()


def obtener_info_producto(url):
    if not url.startswith("https://www.voidstore.cl/"):
        return None

    response = s.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encuentra el primer div con clase "col-md-6"
    main_div = soup.find_all('div', {'class': 'col-md-6'})[0]
    if not main_div:
        return {'title': 'Información no disponible', 'price': 0, 'in_stock': False}

    # Buscar el título del producto
    product_title_element = main_div.find('h1', {'class': 'page-header m-0 text-left'})
    product_title = product_title_element.text.strip() if product_title_element else 'No se encontró el título'

    # Buscar el precio del producto
    price_wrapper = main_div.find('div', {'class': 'form-price_desktop'})
    final_price = '0'
    if price_wrapper:
        final_price_element = price_wrapper.find('span', {'class': 'product-form-price form-price'})
        if final_price_element:
            final_price = final_price_element.text.strip().replace('$', '').replace('.', '')

    # Verificar la disponibilidad del producto
    out_of_stock_div = main_div.find('div', {'class': 'product-stock product-out-stock visible'})
    in_stock = not out_of_stock_div  # Si el div "Agotado" no está presente, el producto tiene stock

    total_price = int(final_price)

    return {'title': product_title, 'price': total_price, 'in_stock': in_stock}


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
