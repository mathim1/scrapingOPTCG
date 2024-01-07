import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onePieceTCG.settings")

import django
django.setup()

from requests_html import HTMLSession
from bs4 import BeautifulSoup
from catalog.models import Producto, Moneda

s = HTMLSession()

def obtener_info_producto(url):
    r = s.get(url)
    r.html.render(sleep=0)
    soup = BeautifulSoup(r.html.html, 'html.parser')

    # Obtener el título
    product_title_element = soup.find('span', {'id': 'productTitle'})
    product_title = product_title_element.text.strip() if product_title_element else 'No se encontró el título'

    # Encontrar el precio sin el formato de coma
    price_whole_element = soup.find('span', {'class': 'a-price-whole'})
    price_whole = price_whole_element.text.strip().replace(',', '') if price_whole_element else '0'

    # Intentar encontrar el precio de envío
    delivery_price_element = soup.find('span', {'data-csa-c-type': 'element', 'data-csa-c-content-id': 'DEXUnifiedCXPDM'})
    if delivery_price_element and 'data-csa-c-delivery-price' in delivery_price_element.attrs:
        delivery_price = delivery_price_element['data-csa-c-delivery-price'].strip().replace('¥', '').replace(',', '')
    else:
        delivery_price_element = soup.find('div', {'id': 'mir-layout-DELIVERY_BLOCK-slot-NO_PROMISE_UPSELL_MESSAGE'})
        if delivery_price_element:
            delivery_price = delivery_price_element.text.split()[0].strip().replace('¥', '').replace(',', '')
        else:
            delivery_price = '0'

    # Calcular el precio total
    if price_whole == '0' or delivery_price == '0':
        total_price = 0
    else:
        total_price = int(float(price_whole) + float(delivery_price))

    return {'title': product_title, 'price': total_price}

# Primero obtenemos el id de la moneda JPY
moneda_jpy = Moneda.objects.get(moneda='JPY')

# Luego obtenemos todos los productos que tengan esa moneda
productos = Producto.objects.filter(moneda=moneda_jpy)

# Iterar sobre los productos y actualizar la información en la base de datos
for producto in productos:
    info_producto = obtener_info_producto(producto.url)

    # Imprimir la información obtenida
    print(f'Título para {producto.nombre}: {info_producto["title"]}')
    print(f'Precio Total para {producto.nombre}: {info_producto["price"]}')
    print('---')

    # Actualizar el campo de precio en la base de datos
    producto.precio = info_producto['price']
    producto.save()
