from time import sleep
import re
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import re

class KijijiScraper():
    
    def __init__(self, base_url: str, start_link: str, file_name: str) :
        
        self.file_name = file_name
        self.base_url = base_url
        self.start_link = start_link
        self.item_links = []
        self.pages_links = [start_link]
        self.df = pd.DataFrame(columns=['Title','Breadcrumb','Date Posted','Address', 'latitude', 'longitude', 'locality', 'region', 'Pictures','Description','Phone No','Email','Price','Link'])
        self.start_scraping()
    
    
    def start_scraping(self):
        
        # start scraping
        next_page = self.start_link
        while next_page: 
            
            self.get_items_links(next_page)
            
            self.scrape_info()
                
            next_page = self.get_next_page(next_page)
            
            if next_page is None:
                print('next page None')
                break
          
                     
    def get_items_links(self, page_link):
        """This method will grab all the links of items on a provided page link 
        and it will save into self.item_links
        """
        response = get(page_link)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        total_items=[self.base_url+link['href'] for link in html_soup.find_all('a' , attrs={'class': 'title'}) ]
        self.item_links.extend(total_items)
       
         
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
                print('--------Next Page Found ALready')
                return None
        except Exception as er:
            print('Error in getting next page')
            print('Error:', er)
            print('page:', page_link)
            return None
        
    
    def scrape_info(self):
        """This method will scrape all the info of each item in self.item_links and will save it into dataframe
        """
        print('Scraping Info of page No:', len(self.pages_links))
        print(len(self.item_links))
        
        
        for item in self.item_links:
            
            print('--------------Link:', item)
            try:
                response = get(item)
                html_soup = BeautifulSoup(response.text, 'html.parser')
                
                title = html_soup.find('h1' , attrs={'class': 'title-2323565163'}).get_text() if html_soup.find('h1' , attrs={'class': 'title-2323565163'}) is not None else 'N/A'
                bread_crumbs = html_soup.find('div' , attrs={'class': 'breadcrumbs-320621489'}).get_text()  if html_soup.find('div' , attrs={'class': 'breadcrumbs-320621489'})is not None else 'N/A'
                date_posted = html_soup.find('div' , attrs={'class': 'datePosted-383942873'}).get_text() if html_soup.find('div' , attrs={'class': 'datePosted-383942873'}) is not None else 'N/A'
                address = html_soup.find('span' , attrs={'class': 'address-3617944557'}).get_text() if html_soup.find('span' , attrs={'class': 'address-3617944557'}) is not None else 'N/A'
                latitude = html_soup.find('meta' , attrs={'property': 'og:latitude'})['content'] if html_soup.find('meta' , attrs={'property': 'og:latitude'}) is not None else 'N/A'
                longitude = html_soup.find('meta' , attrs={'property': 'og:longitude'})['content'] if html_soup.find('meta' , attrs={'property': 'og:longitude'})  is not None else 'N/A'
                locality = html_soup.find('meta' , attrs={'property': 'og:locality'})['content'] if html_soup.find('meta' , attrs={'property': 'og:locality'})  is not None else 'N/A'
                region = html_soup.find('meta' , attrs={'property': 'og:region'})['content'] if html_soup.find('meta' , attrs={'property': 'og:region'}) is not None else 'N/A'
                pictures = [ img['src'] for img in html_soup.find_all('img', attrs={'class': 'image-3484370594 heroImageBackground-2776220296'}) ]
                description = html_soup.find('div' , attrs={'itemprop': 'description'}).get_text() if html_soup.find('div' , attrs={'itemprop': 'description'}) is not None else 'N/A'
                try:
                    phone_no = re.findall(r"((?:\+\d{2}[-\.\s]??|\d{4}[-\.\s]??)?(?:\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}))", description)
                    # phone_no = phone_regex.search(str(description)).group()
                except:
                    phone_no = 'N/A'

                try:
                    email = re.findall(r"(\b[\w.]+@+[\w.]+.+[\w.]\b)", description)
                    # email = email_regex.search(str(description)).group()
                except:
                    email = 'N/A'
                
                price =  html_soup.find('div' , attrs={'class': 'priceContainer-1419890179'}).get_text() if html_soup.find('div' , attrs={'class': 'priceContainer-1419890179'}) is not None else 'N/A'
                
                # print('Title:', title)
                # print('bread_crumbs:', bread_crumbs)
                # print('date_posted:', date_posted)
                # print('address:', address)
                # print('latitude:', latitude)
                # print('longitude:', longitude)
                # print('locality:', locality)
                # print('region:', region)
                # print('pictures:', len(pictures))
                # print('description:', description)
                # print('phone_no:', phone_no)
                # print('email:', email)
                # print('Price:', price)
                # print('Link:', item)
                
                to_append = [title, bread_crumbs, date_posted, address, latitude, longitude, locality, region, \
                            pictures, description, phone_no, email, price, item ]
            
                if not self.append_row(to_append):
                    print('error in appending row')
                
            except:
                print('Error for link:', item)
            
        
        
        self.df.to_excel(self.file_name + ".xlsx") 
        self.item_links = []
    
    
    def append_row(self, to_append: list) -> bool:
        try:
            a_series = pd.Series(to_append, index = self.df.columns)
            self.df = self.df.append(a_series, ignore_index=True)
            return True
        except:
            return False
    
    
    
base_url = 'https://www.kijiji.ca'
buysell_link = 'https://www.kijiji.ca/b-buy-sell/ontario/c10l9004'  #buy and sell
car_link = 'https://www.kijiji.ca/b-cars-vehicles/mississauga-peel-region/c27l1700276'  #buy and sell
services = 'https://www.kijiji.ca/b-services/mississauga-peel-region/c72l1700276'  #buy and sell


buy_sell =  KijijiScraper(base_url=base_url, start_link=buysell_link, file_name= 'Buy and Sell')
buy_sell.start_scraping()

# car = KijijiScraper(base_url=base_url, start_link=car_link, file_name= 'Car and vehicles')
# car.start_scraping()

# services = KijijiScraper(base_url=base_url, start_link=services, file_name= 'Services')
# services.start_scraping()