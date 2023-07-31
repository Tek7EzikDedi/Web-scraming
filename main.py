from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
import lxml

URL = "https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.70318068457031%2C%22east%22%3A-122.16347731542969%2C%22south%22%3A37.61800196820299%2C%22north%22%3A37.932247013814965%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"

################################-----BeatifulSoup-----###########################
URL_form = "https://docs.google.com/forms/d/e/1FAIpQLSd27nsuYPCmbM7OBE6k0JUJ1oc9HC_umLeuMGnjiN0dsGkOig/viewform?usp=sf_link"

headers = { 'Accept-Language' : "tr-TR,tr;q=0.9",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}


respnse = requests.get(URL, headers=headers)
data = respnse.text

soup = BeautifulSoup(data, "lxml")

value_data = soup.select(selector=".StyledPropertyCardDataArea-c11n-8-85-1__sc-yipmu-0 span")
value_list = []
for i in value_data:
    value = i.getText()
    if value[6] == "/":
        new_value = value.split("/")
        value_list.append(new_value[0])
    else:
        new_value = value.split("+")
        value_list.append(new_value[0])

adres_list = []
links_list = []
links = soup.select(selector=(".StyledPropertyCardDataWrapper-c11n-8-85-1__sc-1omp4c3-0 a"))
for i in links:
    adres = i.getText().split("|")
    if len(adres) == 2:
        adres_list.append(adres[1])
    else:
        adres_list.append(adres[0])
    link = i.get("href")
    if link[0] != "h":
        new_link = "https:/" + link
        links_list.append(new_link)
    else:
        links_list.append(link)
################################-----BeatifulSoup-----###########################

################################-----Selenium-----###########################

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

driver.get(URL_form)


rep = len(links_list)
while rep > 0:
    time.sleep(1)
    form_adres = driver.find_element(By.XPATH,
                                     '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    form_price = driver.find_element(By.XPATH,
                                     '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    form_link = driver.find_element(By.XPATH,
                                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    form_adres.send_keys(adres_list[-rep])
    form_price.send_keys(value_list[-rep])
    form_link.send_keys(links_list[-rep])
    send = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span').click()
    time.sleep(1)
    another = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a').click()
    time.sleep(2)
    rep -= 1