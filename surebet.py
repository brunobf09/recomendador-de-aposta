# importando biblioteca
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
import pandas as pd

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver =webdriver.Chrome('chromedriver',chrome_options=chrome_options)


driver.get('https://www.betfair.com/exchange/plus/pt/futebol/brasil-s%C3%A9rie-a-apostas-13')
<<<<<<< HEAD

while (len(driver.find_elements(By.ID,"onetrust-accept-btn-handler"))) < 1:
    sleep(0.5)
=======
>>>>>>> 9174d1fe4c34c79ba08366b94ba808d11a2e2cb5

while (len(driver.find_elements(By.ID,"onetrust-accept-btn-handler"))) < 1:
    sleep(0.5)

accept = driver.find_element(By.ID,"onetrust-accept-btn-handler")    
accept.click()
sleep(1)


teams = []
under_over = []
odds_events = []

for odds in driver.find_elements(By.CLASS_NAME, 'bet-button-price'):
    odds_events.append(odds.text)
for team in driver.find_elements(By.CLASS_NAME, 'name'):
    teams.append(team.text)

driver.quit()
#
odd = odds_events[::6]
home = teams[::2]
away = teams[1::2]
#
#
betfair = {'Home':home,
           'Away':away,
           'Odd_Betfair':odd}
#
#
betfair_df = pd.DataFrame(betfair)
#
betfair_df.to_json('betfair')
