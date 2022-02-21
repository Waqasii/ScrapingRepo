from time import sleep
import csv
import os.path
from collections import defaultdict
import re
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import re

class KijijiScraper():
    
    def __init__(self, base_url: str, start_link: str) -> None:
        self.base_url = base_url
        self.start_link = start_link
        self.item_links = []
        self.pages_links = [start_link]
        self.df = pd.DataFrame(columns=['Title','Breadcrumb','Date Posted','Address','Pictures','Description','Phone No','Email','Price','Link'])
        
        self.get_items_links(self.start_link)
    
    
    def get_items_links(self, page_link):
        """This method will grab all the links of items on a provided page link 
        and it will save into self.item_links
        """
        response = get(page_link)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        total_items=[self.base_url+link['href'] for link in html_soup.find_all('a' , attrs={'class': 'title'}) ]
        self.item_links.extend(total_items)
        
        # get the next page link if available else finish
        next_page = self.get_next_page(page_link=page_link)
        if next_page:
            # self.scrape_info()
            self.get_items_links(next_page)
        else:
            self.scrape_info()

        print('Total Pages:', len(self.pages_links))
    
    
    def get_next_page(self, page_link):
        """This method will return the next_page link if found else None
        """
        response = get(page_link)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        
        try:
            next_page = self.base_url + html_soup.find_all('a' , attrs={'title': 'Next'})[0]['href']
            if next_page not in self.pages_links:
                self.pages_links.append(next_page)
                print('Page No:', len(self.pages_links))
                
                return next_page
            else:
                return None
        except:
            return None
        
    
    def scrape_info(self):
        """This method will scrape all the info of each item and will save it into dataframe
        """
        print('In Scrape Info')
        
        for item in self.item_links:
            print('--------------Link:', item)
            
            response = get(item)
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
            
            price = html_soup.find('div' , attrs={'class': 'priceContainer-1419890179'}).text
            


    
            

            print('Title:', title)
            print('bread_crumbs:', bread_crumbs)
            print('date_posted:', date_posted)
            print('address:', address)
            print('pictures:', len(pictures))
            print('description:', description)
            print('phone_no:', phone_no)
            print('email:', email)
            print('Price:', price)
            print('Link:', item)
            
            break
    



base_url = 'https://www.kijiji.ca'
# start_link = 'https://www.kijiji.ca/b-buy-sell/ontario/c10l9004'  #buy and sell
start_link = 'https://www.kijiji.ca/b-buy-sell/ontario/c10l9004'  #buy and sell
KijijiScraper(base_url=base_url, start_link=start_link)