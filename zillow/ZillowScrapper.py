from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import ast


class ZillowScrapper:
    
    def __init__(self,start_link):
        self.current_link=start_link
        self.visited_link=[]
        
        print('Scrapping Start')
        
        # Set Header
        self.header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'referer': start_link
        
        }
        # try:
        # get total pages first
        total_pages = self.getPagelinks(start_link)
        print('Total Pages:', len(total_pages))
        
       
        # now get house from each page
        self.getInfo(total_pages)
        
        # except:
        # self.df.to_excel("output.xlsx") 
            
    
    def getInfo(self, total_pages):
        
        for page in total_pages:
            response = get(url=page,headers=self.header)
            html_soup = BeautifulSoup(response.text, 'html.parser')
            
            # total houses on this page
            total_places=html_soup.find_all('article' , attrs={'class': 'list-card', })
            print('Total House On This Page:',len(total_places))
            
            

               
            # get data from each house
            for place in total_places:
                
                
                house_price = place.find('div' , attrs={'class': 'list-card-price', }).text
                print('house_price: ', house_price)
                
                house_detail = place.find('ul' , attrs={'class': 'list-card-details', }).text
                print('house_detail:', house_detail)
                
                house_add = place.find('address' , attrs={'class': 'list-card-addr', }).text
                print('house_add:', house_add)
                
                houses = html_soup.findAll('script', {'type' : 'application/ld+json'})
                houses = ast.literal_eval(houses[0].text)
                
                house_latitude = houses['geo']['latitude']
                house_longitude = houses['geo']['longitude']
                print('latitude:', house_latitude)
                print('longitude:', house_longitude)
                
                house_url = houses['url']
                print('House URL:', house_url)

                break
            
                
    def getPagelinks(self,start_link):
        
        return [start_link]
    
        total_pages = []
        current_page = start_link
        next_page = start_link
        real_links = []
        
        # append the first page link
        total_pages.append(start_link)
        real_links.append(start_link)
        while True:
            try:
                response = get(url=current_page,headers=self.header)
                html_soup = BeautifulSoup(response.text, 'html.parser')
                
                next_page = 'https://www.zillow.com' + html_soup.find('a' , attrs={'title': 'Next page', })['href']
                
                
                if next_page  in total_pages:
                    break
                else:
                    print(next_page)
                    total_pages.append(next_page)
                
            except:
                break
            
            
            
            
            
        return real_links
        
        


#Main Page URL
start_link = 'https://www.zillow.com/homes/for_sale/land_type/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-140.08703075000003%2C%22east%22%3A-113.01671825000003%2C%22south%22%3A47.84160653027041%2C%22north%22%3A60.34792085708892%7D%2C%22mapZoom%22%3A5%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A700000%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22min%22%3A2594%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22lot%22%3A%7B%22min%22%3A43560%7D%2C%22sf%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22watv%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%7D'

#Run Program
ZillowScrapper(start_link)


