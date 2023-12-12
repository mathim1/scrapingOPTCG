import os
import django
from selenium.common import NoSuchElementException, StaleElementReferenceException

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onePieceTCG.settings")
django.setup()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
from selenium.common.exceptions import TimeoutException

from catalog.models import Card

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()


def obtener_precio_menor_modificado(driver, card_name, card_id):
    print(f"Iniciando búsqueda para {card_name} (ID: {card_id}).")
    card_name_url = card_name.replace(" ", "+")
    base_url = "https://www.tcgplayer.com/search/one-piece-card-game/product?productLineName=one-piece-card-game&q="
    search_url = f"{base_url}{card_name_url}&view=grid"

    menor_precio = float('inf')
    pagina_actual = 1

    while True:
        driver.get(f"{search_url}&page={pagina_actual}")
        print(f"Accediendo a la página {pagina_actual} de búsqueda específica en TCGPlayer.")

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.search-result"))
            )

            resultados = driver.find_elements(By.CSS_SELECTOR,
                                              "section.search-result__product.search-result__product__add-to-cart")

            for resultado in resultados:
                try:
                    carid_element = resultado.find_element(By.CSS_SELECTOR,
                                                           "section.search-result__rarity span:last-child").text
                    if card_id in carid_element:
                        precio_element = resultado.find_element(By.CSS_SELECTOR,
                                                                "span.search-result__market-price--value")
                        precio = float(re.sub("[^\d\.]", "", precio_element.text))

                        if precio < menor_precio:
                            menor_precio = precio
                except NoSuchElementException:
                    continue
                except StaleElementReferenceException:
                    continue

            try:
                next_buttons = driver.find_elements(By.CSS_SELECTOR, "div.tcg-pagination__pages a")
                if len(next_buttons) > pagina_actual:
                    pagina_actual += 1
                else:
                    break
            except NoSuchElementException:
                break
            except StaleElementReferenceException:
                continue

        except TimeoutException:
            print(
                f"Tiempo de espera excedido. No se encontraron resultados para {card_name} (ID: {card_id}) en la página {pagina_actual}.")
            return None
        except StaleElementReferenceException:
            continue

    return menor_precio if menor_precio != float('inf') else None


cartas = Card.objects.all()
for carta in cartas:
    precio = obtener_precio_menor_modificado(driver, carta.name, carta.carid)
    if precio:
        carta.price = precio
        carta.save()
        print(f"Precio actualizado para {carta.name} (ID: {carta.carid}): {precio}")
    else:
        print(f"No se encontró precio para {carta.name} (ID: {carta.carid}).")

driver.quit()
