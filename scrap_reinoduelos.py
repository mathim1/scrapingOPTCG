import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onePieceTCG.settings")

import django

django.setup()

from urllib.parse import urlparse
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from catalog.models import Producto, Moneda

s = HTMLSession()


def obtener_info_producto(url):
    # Verificar que la URL comience con la base deseada
    if not url.startswith("https://elreinodelosduelos.cl/"):
        return None

    # Usar la sesión para manejar la solicitud
    r = s.get(url)
    # Ejecutar JavaScript si es necesario
    r.html.render(sleep=1)
    # Parsear el HTML renderizado
    soup = BeautifulSoup(r.html.html, 'html.parser')

    # Obtener el título del producto del elemento H1
    product_title_element = soup.find('h1', {'class': 'product_title entry-title wd-entities-title'})
    product_title = product_title_element.text.strip() if product_title_element else 'No se encontró el título'

    # Encontrar el precio en el elemento <p> con la clase 'price'
    price_element = soup.find('p', {'class': 'price'})
    if price_element:
        final_price_element = price_element.find('bdi')
        if final_price_element:
            final_price = final_price_element.text.strip()
            # Eliminar el símbolo del dólar y los puntos para quedarnos solo con números
            final_price = final_price.replace('$', '').replace('.', '')
        else:
            final_price = '0'
    else:
        final_price = '0'

    # Convertir el precio a un entero
    total_price = int(final_price)

    return {'title': product_title, 'price': total_price}


# Obtener el ID de la moneda CLP
moneda_clp = Moneda.objects.get(moneda='CLP')

# Obtener todos los productos con esa moneda
productos = Producto.objects.filter(moneda=moneda_clp)

# Iterar sobre los productos y actualizar la información en la base de datos
for producto in productos:
    # Solo procesar el producto si la URL base es la correcta
    info_producto = obtener_info_producto(producto.url)
    if info_producto:
        # Imprimir la información obtenida
        print(f'Título para {producto.nombre}: {info_producto["title"]}')
        print(f'Precio Total para {producto.nombre}: {info_producto["price"]}')
        print('---')

        # Actualizar el campo de precio en la base de datos
        producto.precio = info_producto['price']
        producto.save()
