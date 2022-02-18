from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from parsel import Selector
import csv
import os.path
from collections import defaultdict
import re
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from lxml import etree


start_link = 'https://www.kijiji.ca/v-renovation-cabinet-counter/city-of-toronto/custom-kitchen-cabinets-and-bathroom-vanities-10-off/1605096858'

response = get(start_link)
html_soup = BeautifulSoup(response.text, 'html.parser')

title = html_soup.find('h1' , attrs={'class': 'title-2323565163'}).text
bread_crumbs = html_soup.find('div' , attrs={'class': 'breadcrumbs-320621489'}).text
date_posted = html_soup.find('div' , attrs={'class': 'datePosted-383942873'}).text
address = html_soup.find('span' , attrs={'class': 'address-3617944557'}).text
print('Title:', title)
print('bread_crumbs:', bread_crumbs)
print('date_posted:', date_posted)
print('address:', address)


pictures = html_soup.find_all('source' , attrs={'class': None})
print('pictures:', pictures)
