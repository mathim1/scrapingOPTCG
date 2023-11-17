from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

def obtener_info_producto_selenium():
    url = "https://www.guildreams.com/product/one-piece-tcg-pillars-of-strength-booster-pack"

    # Opciones para el navegador (puedes modificarlas según tus necesidades)
    options = webdriver.ChromeOptions()
    options.headless = True  # Ejecutar en modo sin cabeza (sin interfaz gráfica)

    # Inicializar el WebDriver con la ruta específica
    service = Service('C:/Windows/chromedriver-win64/chromedriver.exe') # Ruta al ChromeDriver
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Abrir la página
        driver.get(url)
        time.sleep(5)  # Esperar a que el JavaScript se ejecute

        # Obtener el HTML de la página
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Extraer la información del producto
        product_title = soup.find('h2').get_text(strip=True) if soup.find('h2') else 'No se encontró el título'
        final_price_element = soup.find('span', class_='h2', attrs={'data-bs': 'product.finalPrice'})
        final_price = final_price_element.get_text(strip=True).replace('$', '').replace(' ', '').replace('.', '') if final_price_element else '0'
        total_price = int(final_price)

        return {'title': product_title, 'price': total_price}
    finally:
        driver.quit()

# Uso de la función y mostrar resultados
info_producto = obtener_info_producto_selenium()
print(f'Título: {info_producto["title"]}')
print(f'Precio Total: {info_producto["price"]}')
