from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd
import openpyxl

# FONKSİYONLAR
def login(driver):
    login_button = driver.find_element(By.XPATH, '//a[text()="Login"]')
    login_button.click()

    username = driver.find_element(By.ID, 'username')
    username.send_keys('berkyyd')

    password = driver.find_element(By.ID, 'password')
    password.send_keys('berkayd17')

    login = driver.find_element(By.XPATH, '//input[@value="Login"]')
    login.click()
def wait_for_element(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

# Güncellenmiş ChromeDriver yolu
chrome_driver_path = "C:/path/chromedriver.exe"

# Service objesi ile başlat
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

author_dict = {
    'name': [],
    'birth_day': [],
    'birth_place': []
}

author_urls = []

# login yapıyoruz



url = 'https://quotes.toscrape.com/'
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_experimental_option('detach', True)
driver.get(url)

login(driver)


# Yazarların linklerini alıyoruz
while True:
    quotes = driver.find_elements(By.CLASS_NAME, 'quote')
    for quote in quotes:
        try:
            # Yazar linklerini al
            author_link = quote.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            author_urls.append(author_link)
        except:
            continue

    # Sonraki sayfaya git
    try:
        # Sayfa geçişi için bekleme ekleyelim
        next_button = wait_for_element(driver, By.CSS_SELECTOR, 'li.next a')
        next_button.click()
        sleep(2)  # Sayfanın yüklenmesini bekle
    except:
        break

# Linkleri set'e çevirip tekrarı engelle
author_urls = list(set(author_urls))

# Yazar sayfalarını ziyaret et
for url in author_urls:
    driver.get(url)
    wait_for_element(driver, By.CSS_SELECTOR, 'h3.author-title')  # Yazar sayfasının yüklenmesini bekle

    try:
        name = driver.find_element(By.CSS_SELECTOR, 'h3.author-title').text
        author_dict['name'].append(name)

        birth_day = driver.find_element(By.CSS_SELECTOR, 'span.author-born-date').text
        author_dict['birth_day'].append(birth_day)

        birth_place = driver.find_element(By.CSS_SELECTOR, 'span.author-born-location').text
        author_dict['birth_place'].append(birth_place)
    except Exception as e:
        print(f"Error fetching details for {url}: {e}")

# Veriyi Excel'e kaydedelim
df = pd.DataFrame(author_dict)
df.to_excel('yazarlar.xlsx')

input("Tarayıcıyı kapatmak için ENTER'a bas...")  # Tarayıcıyı açık tut
driver.quit()  # Enter basılınca tarayıcıyı kapat
