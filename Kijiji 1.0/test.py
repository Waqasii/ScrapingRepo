from time import sleep
import csv
import os.path
from collections import defaultdict
import re
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import re
import ast

start_link = 'https://www.kijiji.ca/v-buy-sell-other/ottawa/opi-nail-polish/1523315041'
# start_link = 'https://www.kijiji.ca/v-other-home-appliance/oakville-halton-region/brand-new-500w-portable-power-station-emergency-power/1589915641'

response = get(start_link)
html_soup = BeautifulSoup(response.text, 'html.parser')

title = html_soup.find('h1' , attrs={'class': 'title-2323565163'}).get_text()
bread_crumbs = html_soup.find('div' , attrs={'class': 'breadcrumbs-320621489'}).text
date_posted = html_soup.find('div' , attrs={'class': 'datePosted-383942873'}).text if html_soup.find('div' , attrs={'class': 'datePosted-383942873'}) is not None else 'N/A'
address = html_soup.find('span' , attrs={'class': 'address-3617944557'}).text
pictures = [ img['src'] for img in html_soup.find_all('img') ]
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
price = html_soup.find('div' , attrs={'class': 'priceContainer-1419890179'}).text

    
print('Title:', title)
print('bread_crumbs:', bread_crumbs)
print('date_posted:', date_posted)
print('address:', address)
print('pictures:', pictures)
print(description)
print(phone_no)
print(email)
print('Price:', price)


latitude = html_soup.find('meta' , attrs={'property': 'og:latitude'})['content']
longitude = html_soup.find('meta' , attrs={'property': 'og:longitude'})['content']
locality = html_soup.find('meta' , attrs={'property': 'og:locality'})['content']
region = html_soup.find('meta' , attrs={'property': 'og:region'})['content']

print('latitude:', latitude)
print('longitude:', longitude)
print('locality:', locality)
print('region:', region)


    
