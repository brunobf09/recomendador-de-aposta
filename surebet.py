# importando biblioteca
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
import pandas as pd
import json

def scrapy(league):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('chromedriver', chrome_options=chrome_options)

    link = "https://www.betfair.com/exchange/plus/pt/futebol/"

    driver.get(link)

    while (len(driver.find_elements(By.ID,"onetrust-accept-btn-handler"))) < 1:
        sleep(0.3)

    accept = driver.find_element(By.ID,"onetrust-accept-btn-handler")
    accept.click()

    teams = []
    odds_events = []
    date = []

    for l in league:
        driver.get(link + l)
        while (len(driver.find_elements(By.CLASS_NAME, 'bet-button-price'))) < 1:
            sleep(0.2)
        for odds in driver.find_elements(By.CLASS_NAME, 'bet-button-price'):
            odds_events.append(odds.text)
        for team in driver.find_elements(By.CLASS_NAME, 'name'):
            teams.append(team.text)
        for d in driver.find_elements(By.CLASS_NAME, 'label'):
            date.append(d.text)

    driver.quit()

    odd = odds_events[::6]
    home = teams[::2]
    away = teams[1::2]

    betfair = {'Date': date,
               'HomeTeam':home,
               'AwayTeam':away,
               'Odd_Betfair':odd}

    betfair_df = pd.DataFrame(betfair)
    times = json.load(open('times.json'))
    betfair_df.HomeTeam = betfair_df.HomeTeam.map(times)
    betfair_df.AwayTeam = betfair_df.AwayTeam.map(times)

    return betfair_df.to_json('betfair')

# def data():
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument('--headless')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')
#     driver = webdriver.Chrome('chromedriver', chrome_options=chrome_options)

#     link = "https://www.betfair.com/exchange/plus/pt/futebol-apostas-1/tomorrow"
#     driver.get(link)

#     while (len(driver.find_elements(By.ID, "onetrust-accept-btn-handler"))) < 1:
#         sleep(0.2)

#     driver.find_element(By.ID, "onetrust-accept-btn-handler").click()

#     while (len(driver.find_elements(By.CLASS_NAME, "selected-option"))) < 1:
#         sleep(0.2)

#     driver.find_element(By.CLASS_NAME, "selected-option").click()
#     driver.find_elements(By.CLASS_NAME, "option-list-item")[1].click()

#     teams = []
#     odds_events = []
#     date = []

#     while (len(driver.find_elements(By.CLASS_NAME, 'bet-button-price'))) < 1:
#         sleep(0.2)

#     for odds in driver.find_elements(By.CLASS_NAME, 'bet-button-price'):
#         odds_events.append(odds.text)
#     for team in driver.find_elements(By.CLASS_NAME, 'name'):
#         teams.append(team.text)
#     for d in driver.find_elements(By.CLASS_NAME, 'label'):
#         date.append(d.text)
#     driver.find_element(By.CLASS_NAME, "coupon-page-navigation__label--next").click()

#     while len(driver.find_elements(By.CLASS_NAME, "is-disabled")) == 0:
#         while (len(driver.find_elements(By.CLASS_NAME, 'bet-button-price'))) < 1:
#             sleep(0.2)
#         for odds in driver.find_elements(By.CLASS_NAME, 'bet-button-price'):
#             odds_events.append(odds.text)
#         for team in driver.find_elements(By.CLASS_NAME, 'name'):
#             teams.append(team.text)
#         for d in driver.find_elements(By.CLASS_NAME, 'label'):
#             date.append(d.text)
#         driver.find_element(By.CLASS_NAME, "coupon-page-navigation__label--next").click()

#     driver.quit()

#     odd = odds_events[::6]
#     home = teams[::2]
#     away = teams[1::2]

#     betfair = {'HomeTeam': home,
#                'AwayTeam': away,
#                'Odd_Betfair': odd}

#     betfair_df = pd.DataFrame(betfair)
#     times = json.load(open('times.json'))
#     betfair_df.HomeTeam = betfair_df.HomeTeam.map(times)
#     betfair_df.AwayTeam = betfair_df.AwayTeam.map(times)

#     return betfair_df.to_json('betfair_tw')
