# importando biblioteca
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
import pandas as pd
import os
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

driver.get('https://www.betfair.com/exchange/plus/pt/futebol/brasil-s%C3%A9rie-a-apostas-13')
sleep(20)

accept = driver.find_element(By.ID,"onetrust-accept-btn-handler")
accept.click()
sleep(3)


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
