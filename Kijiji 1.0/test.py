from time import sleep
import csv
import os.path
from collections import defaultdict
import re
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import re

start_link = 'https://www.kijiji.ca/v-renovation-cabinet-counter/city-of-toronto/custom-kitchen-cabinets-and-bathroom-vanities-10-off/1605096858'

response = get(start_link)
html_soup = BeautifulSoup(response.text, 'html.parser')

title = html_soup.find('h1' , attrs={'class': 'title-2323565163'}).text
bread_crumbs = html_soup.find('div' , attrs={'class': 'breadcrumbs-320621489'}).text
date_posted = html_soup.find('div' , attrs={'class': 'datePosted-383942873'}).text
address = html_soup.find('span' , attrs={'class': 'address-3617944557'}).text
pictures = html_soup.find_all('img')
description = html_soup.find('div' , attrs={'itemprop': 'description'}).text
try:
    phone_no = re.findall(r"((?:\+\d{2}[-\.\s]??|\d{4}[-\.\s]??)?(?:\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}))", description)
    # phone_no = phone_regex.search(str(description)).group()
except:
    phone_no = 'None'

try:
    email = re.findall(r"(\b[\w.]+@+[\w.]+.+[\w.]\b)", description)
    # email = email_regex.search(str(description)).group()
except:
    email = 'None'
    
print('Title:', title)
print('bread_crumbs:', bread_crumbs)
print('date_posted:', date_posted)
print('address:', address)
print('pictures:', pictures[0]['src'])
print(description)
print(phone_no)
print(email)



    
