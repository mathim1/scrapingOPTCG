import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onePieceTCG.settings")

import django

django.setup()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from collections import Counter
from urllib.parse import unquote
import threading
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from catalog.models import Card


def obtener_precio(carta_id):
    try:
        carta = Card.objects.get(carid=carta_id)
        return carta.price
    except Card.DoesNotExist:
        return 0


def extraer_cartas_desde_url_selenium(url, semaphore, chrome_driver_path):
    with semaphore:
        service = Service(chrome_driver_path)
        driver = webdriver.Chrome(service=service)

        try:
            url_decodificada = unquote(url)
            driver.get(url_decodificada)

            # Esperar a que el elemento esté presente
            wait = WebDriverWait(driver, 30)  # Espera hasta 30 segundos
            textarea = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'textarea')))

            texto_decodificado = unquote(textarea.text)
            cartas = eval(texto_decodificado)
            cartas = [carta for carta in cartas if not carta.startswith("Exported from onepiecetopdecks.com")]
            return cartas
        except Exception as e:
            print(f"Error al obtener datos de {url}: {e}")
            return []
        finally:
            driver.quit()


def extraer_cartas_en_thread(url, resultados, semaphore, chrome_driver_path):
    cartas = extraer_cartas_desde_url_selenium(url, semaphore, chrome_driver_path)
    resultados[url] = cartas


def clasificar_cartas(cartas):
    clasificacion = Counter(cartas)
    return clasificacion


def extraer_set_de_carta(carid):
    return carid.split('-')[0]


def calcular_valor_deck(clasificacion):
    detalles_cartas = {}
    precios_por_set = {}
    total_valor = 0

    for carta_id, cantidad in clasificacion.items():
        try:
            carta = Card.objects.get(carid=carta_id)
            precio = carta.price
            nombre_carta = carta.name
        except Card.DoesNotExist:
            precio = 0
            nombre_carta = f"Carta Desconocida (ID: {carta_id})"

        set_carta = extraer_set_de_carta(carta_id)
        total_valor += precio * cantidad
        precios_por_set.setdefault(set_carta, 0)
        precios_por_set[set_carta] += precio * cantidad

        detalles_cartas[carta_id] = {
            'nombre': nombre_carta,
            'set': set_carta,
            'cantidad': cantidad,
            'precio_individual': precio,
            'precio_total': precio * cantidad
        }

    return total_valor, detalles_cartas, precios_por_set


def obtener_urls_de_usuario():
    print("Por favor, ingresa las URLs separadas por una nueva línea. Escribe 'fin' para terminar.")
    urls = []
    while True:
        url = input().strip()  # Eliminar espacios en blanco al principio y al final
        if url.lower() == 'fin':
            break
        if url:  # Añadir la URL solo si no está vacía
            urls.append(url)
    return urls


def main():
    chrome_driver_path = ChromeDriverManager().install()
    urls = obtener_urls_de_usuario()  # Obtener URLs del usuario

    resultados = {}
    hilos = []
    semaphore = threading.Semaphore(5)  # Limitar a 5 hilos activos simultáneamente

    # Crear y comenzar los hilos
    for url in urls:
        hilo = threading.Thread(target=extraer_cartas_en_thread, args=(url, resultados, semaphore, chrome_driver_path))
        hilos.append(hilo)
        hilo.start()

    # Esperar a que todos los hilos terminen
    for hilo in hilos:
        hilo.join()

    informacion_decks = []

    # Recolectar la información de cada deck
    for url, cartas in resultados.items():
        clasificacion_deck = clasificar_cartas(cartas)
        valor_deck, detalles_cartas, precios_por_set = calcular_valor_deck(clasificacion_deck)
        informacion_decks.append((url, valor_deck, detalles_cartas, precios_por_set))

    # Ordenar los decks por el valor total y luego imprimir
    for url, valor_deck, detalles_cartas, precios_por_set in sorted(informacion_decks, key=lambda x: x[1]):
        print(f"URL: {url}\nValor total del deck: ${valor_deck:.2f}\n")
        print("Detalles de las Cartas:")
        for carta_id, detalles in sorted(detalles_cartas.items(), key=lambda item: item[1]['precio_total']):
            print(
                f"Carta: {detalles['nombre']} (ID: {carta_id}), Set: {detalles['set']}, Cantidad: {detalles['cantidad']}, Precio Individual: ${detalles['precio_individual']:.2f}, Precio Total: ${detalles['precio_total']:.2f}")

        print("\n--------------\nPrecios por Set:")
        for set_carta, precio_total in sorted(precios_por_set.items(), key=lambda item: item[1]):
            print(f"Set: {set_carta}, Precio Total: ${precio_total:.2f}")

        print("\n--------------")


if __name__ == "__main__":
    main()
