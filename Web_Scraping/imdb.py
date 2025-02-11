from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import pandas as pd
import openpyxl

movie_dict = {
    'name': [],
    'year': [],
    'duration': [],
    'stars': [],
    'votes': [],
    'metascore': [],
    'description': []
}

# FONKSİYONLAR
def accept_cookies(driver):
    try:
        accept_cookies = driver.find_element(By.XPATH, '//button[text()="Accept"]')
        accept_cookies.click()
    except:
        pass

# Güncellenmiş ChromeDriver yolu
chrome_driver_path = "C:/path/chromedriver.exe"

url = 'https://www.imdb.com'
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_experimental_option('detach', True)

# Service objesi ile başlat
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)
actions = ActionChains(driver)
driver.implicitly_wait(3)
driver.get(url)

sleep(5)

accept_cookies(driver)

sleep(2)

search_button = driver.find_element(By.ID, 'suggestion-search-button')
actions.move_to_element(search_button).perform()
# yukarıdaki kod tıklanma sorunu varsa çözüyor
search_button.click()

sleep(2)

movie_tv = driver.find_element(By.CSS_SELECTOR, 'a[data-testid="advanced-search-chip-tt"]')
actions.move_to_element(movie_tv).perform()
movie_tv.click()

sleep(5)

#title_type = driver.find_element(By.XPATH, '//div[text()="Title type"]')
#title_type.click()

movie = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="test-chip-id-movie"]')
actions.move_to_element(movie).perform()
movie.click()

sleep(1)

comedy = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="test-chip-id-Comedy"]')
actions.move_to_element(comedy).perform()
comedy.click()

sleep(1)

awards = driver.find_element(By.ID, 'awardsAccordion')
actions.move_to_element(awards).perform()
awards.click()

sleep(1)

oscar = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="test-chip-id-oscar-nominated"]')
actions.move_to_element(oscar).perform()
oscar.click()

sleep(1)

results = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="adv-search-get-results"]')
driver.execute_script('arguments[0].click()', results)
# actions işe yaramazsa bu scriptle yapabiliriz

while True:
    sleep(2)
    more_buttons = driver.find_elements(By.CSS_SELECTOR, 'span.ipc-see-more__text')
    if len(more_buttons) != 0:
        more_button = more_buttons[0]
        actions.move_to_element(more_button).perform()
        more_button.click()
    else:
        break


movies = driver.find_elements(By.CLASS_NAME, 'ipc-metadata-list-summary-item')

for movie in movies:
    raw_name = movie.find_element(By.CSS_SELECTOR, 'h3.ipc-title__text').text
    name = ' '.join(raw_name.split(' ')[1:])
    print(name)
    movie_dict['name'].append(name)

    year = movie.find_elements(By.CSS_SELECTOR, 'span.dli-title-metadata-item')[0].text
    print(year)
    movie_dict['year'].append(year)

    duration = movie.find_elements(By.CSS_SELECTOR, 'span.dli-title-metadata-item')[1].text
    print(duration)
    movie_dict['duration'].append(duration)

    stars = movie.find_element(By.CSS_SELECTOR, 'span.ipc-rating-star--rating').text
    print(stars)
    movie_dict['stars'].append(stars)

    votes = movie.find_element(By.CLASS_NAME, 'ipc-rating-star--voteCount').text.strip()[1:-1]
    print(votes)
    movie_dict['votes'].append(votes)

    try:
        metascore = movie.find_element(By.CSS_SELECTOR, 'span.metacritic-score-box').text
    except:
        metascore = 'Bilgi yok'
    print(metascore)
    movie_dict['metascore'].append(metascore)

    description = movie.find_element(By.CSS_SELECTOR, 'div.ipc-html-content-inner-div').text
    print(description)
    movie_dict['description'].append(description)
    print('\n')

df = pd.DataFrame(movie_dict)
df.to_excel('filmler.xlsx')



input('Enter ile çıkış yap')
driver.quit()