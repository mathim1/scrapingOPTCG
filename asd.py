from selenium import webdriver

driver = webdriver.Chrome() # o webdriver.Firefox() si usas GeckoDriver
driver.get("http://www.google.com")
print(driver.title)
driver.quit()
