from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

#Main Page URL
start_link = 'https://www.zillow.com/homes/for_sale/land_type/'
driver = webdriver.Chrome()
driver.get(start_link)


# response = get(start_link)
html = driver.execute_script("return document.documentElement.outerHTML")
html_soup = BeautifulSoup(html, 'html.parser')
# print(response.text)
total_places=html_soup.find_all('article' , attrs={'class': 'list-card list-card-additional-attribution list-card-additional-attribution-space list-card_not-saved'})
print('total_places:', len(total_places))
