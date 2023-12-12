import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onePieceTCG.settings")
import django

django.setup()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from catalog.models import Card, Moneda  # Asegúrate de importar los modelos correctos

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Abre la página web
driver.get("https://onepiece-cardgame.dev/cards")
driver.maximize_window()

WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.MuiBox-root.css-1xdp8rh"))
)

cards = driver.find_elements(By.CSS_SELECTOR, "div.MuiBox-root.css-1xdp8rh")
moneda = Moneda.objects.get(id=1)

for card in cards:
    try:
        ActionChains(driver).move_to_element(card).perform()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(card))

        driver.execute_script("arguments[0].click();", card)

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[text()='Name']/following-sibling::div"))
        )

        name = driver.find_element(By.XPATH, "//div[text()='Name']/following-sibling::div").text
        card_id = driver.find_element(By.XPATH, "//div[text()='Card ID']/following-sibling::div").text

        # Verifica si ya existe una carta con el mismo carid
        if not Card.objects.filter(carid=card_id).exists():
            new_card = Card(name=name, carid=card_id, moneda=moneda, price=0)
            new_card.save()
        else:
            print(f"La carta con carid {card_id} ya existe, no se creará una nueva.")

    except Exception as e:
        print(f"Error al procesar la carta: {e}")

driver.quit()

print("Datos guardados en la base de datos.")
