from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import pandas as pd
import openpyxl

# drama kategorisinde "Best Director" ödülünü alan yönetmenlerin boylarını kaydetme

# fonksiyonlar
def accept_cookies(driver):
    try:
        accept_cookies = driver.find_element(By.XPATH, '//button[text()="Accept"]')
        accept_cookies.click()
    except:
        pass


url = "https://www.imdb.com/search/title/"

# veriyi kaydetmek için dictionary
director_dict = {
    'name': [],
    'height': []
}

chrome_driver_path = "C:/path/chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_experimental_option('detach', True)

# Service objesi ile başlat
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(5)
actions = ActionChains(driver)
driver.implicitly_wait(3)
driver.get(url)


# cookies çıkarsa kabul edicez
accept_cookies(driver)

sleep(2)

drama = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="test-chip-id-Drama"]')
actions.move_to_element(drama).perform()
drama.click()

sleep(1)

awards = driver.find_element(By.ID, 'awardsAccordion')
actions.move_to_element(awards).perform()
awards.click()

sleep(1)

director = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="test-chip-id-best-director-winning"]')
actions.move_to_element(director).perform()
director.click()

sleep(1)

results = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="adv-search-get-results"]')
actions.move_to_element(results).perform()
results.click()

sleep(1)

while True:
    sleep(2)
    more_buttons = driver.find_elements(By.CSS_SELECTOR, 'span.ipc-see-more__text')
    if len(more_buttons) != 0:
        more_button = more_buttons[0]
        actions.move_to_element(more_button).perform()
        more_button.click()
    else:
        break

director_list = []
infos = driver.find_elements(By.CSS_SELECTOR, 'svg.ipc-icon--info')

for info in infos:
    actions.move_to_element(info).perform()
    info.click()
    sleep(0.5)
    a_tag = driver.find_element(By.CSS_SELECTOR, 'a.clUCBN')
    link = a_tag.get_attribute('href')
    director_list.append(link)
    close = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Close Prompt"]')
    actions.move_to_element(close).perform()
    close.click()
    sleep(0.5)

# yönetmen linklerini tek tek ziyaret edip isim ve boy bilgilerini kaydet

for link in director_list:
    driver.get(link)
    try:
        name = driver.find_element(By.CSS_SELECTOR, 'h1[data-testid="hero__pageTitle"] span[data-testid="hero__primary-text"]').text
    except:
        name = 'Bilgi yok'

    try:
        height = driver.find_element(By.XPATH, '//span[text()="Height"]/following-sibling::div[1]/ul/li/span').text
    except:
        height = 'Bilgi yok'

    director_dict['name'].append(name)
    director_dict['height'].append(height)

# df ile excel formatında kaydet
df = pd.DataFrame(director_dict)
df.to_excel('director.xlsx')


input('Enter a bas kapat')
driver.quit()
