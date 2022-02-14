import requests
from bs4 import BeautifulSoup 

# Set Header
header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
  'referer': 'https://www.zillow.com/homes/for_rent/Manhattan,-New-York,-NY_rb/?searchQueryState=%7B%22pagination'
  
}

# Send a get request:
url = 'https://www.zillow.com/homes/for_rent/Manhattan,-New-York,-NY_rb' 

html = requests.get(url=url,headers=header)
html_soup = BeautifulSoup(html.text, 'html.parser')
total_places=html_soup.find_all('article' , attrs={'class': 'list-card', })

print('Total House On This Page:',len(total_places))