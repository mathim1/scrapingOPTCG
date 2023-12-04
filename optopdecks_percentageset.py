from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from collections import Counter
from urllib.parse import unquote
import threading
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
    clasificacion = Counter()
    for carta in cartas:
        # Excepción para la carta "OP01-025"
        if carta == "OP01-025":
            clasificacion["ST10"] += 1
        else:
            set_code = re.match(r'(.*?)-', carta)
            if set_code:
                clasificacion[set_code.group(1)] += 1
    return clasificacion


def calcular_porcentajes(clasificacion):
    total_cartas = sum(clasificacion.values())
    porcentajes = {set: (count / total_cartas) * 100 for set, count in clasificacion.items()}
    return porcentajes


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

    clasificacion_global = Counter()

    # Procesar los resultados de cada hilo
    for url, cartas in resultados.items():
        clasificacion_deck = clasificar_cartas(cartas)
        porcentajes_deck = calcular_porcentajes(clasificacion_deck)

        print(f"Porcentajes para el deck de la URL {url}:\n", porcentajes_deck)

        clasificacion_global.update(clasificacion_deck)

    # Calcular y mostrar los porcentajes globales
    porcentajes_globales = calcular_porcentajes(clasificacion_global)

    print("\nClasificación global de cartas por set:", clasificacion_global)
    print("Porcentajes globales de cartas por set:", porcentajes_globales)


if __name__ == "__main__":
    main()
