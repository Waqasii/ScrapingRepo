from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver


class ZillowScrapper:
    
    def __init__(self,start_link):
        self.current_link=start_link
        self.visited_link=[]
        self.df = pd.DataFrame(columns=['Title','Type','District','Location','Address','Energy Label','Price','Year Built','Bedrooms','Baths','Living Area','Land Area','Parking Spots','From Shore (m)','Link'])
        print('Scrapping Start')
        self.driver = webdriver.Chrome()
        
        # try:
        self.getInfo()
        # except:
        # self.df.to_excel("output.xlsx") 
            
    
    def getInfo(self):
        if(self.current_link not in self.visited_link):
            self.visited_link.append(self.current_link)
            # print(self.current_link)
            
            
            self.driver = webdriver.Chrome()
            self.driver.get(self.current_link)
            html = self.driver.execute_script("return document.documentElement.outerHTML")
            html_soup = BeautifulSoup(html, 'html.parser')
            total_places=html_soup.find_all('article' , attrs={'class': 'list-card', })
            
            print('Total House On This Page:',len(total_places))
            
            
            for place in total_places:
                
                #get link of each house
                house_link=place.find('a')['href']
                print('house_link: ', house_link)
                
                house_price = place.find('div' , attrs={'class': 'list-card-price', }).text
                print('house_price: ', house_price)
                
                house_detail = place.find('ul' , attrs={'class': 'list-card-details', }).text
                print('house_detail:', house_detail)
                
                house_add = place.find('address' , attrs={'class': 'list-card-addr', }).text
                print('house_add:', house_add)
                break
                
                
    
        


#Main Page URL
start_link = 'https://www.zillow.com/homes/for_sale/land_type/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-140.08703075000003%2C%22east%22%3A-113.01671825000003%2C%22south%22%3A47.84160653027041%2C%22north%22%3A60.34792085708892%7D%2C%22mapZoom%22%3A5%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A700000%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22min%22%3A2594%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22lot%22%3A%7B%22min%22%3A43560%7D%2C%22sf%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22watv%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%7D'

#Run Program
ZillowScrapper(start_link)


