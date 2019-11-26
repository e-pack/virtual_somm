# Import nessesary packages
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import re
import requests
import nltk
from random import randint
from time import sleep
from warnings import warn


# Create collections of search result pages to scrape for 5 popular wine varieties
cab_sauv = 'https://www.winemag.com/?s=&varietal=Cabernet%20Sauvignon&drink_type=wine&page=1&search_type=reviews'
char = 'https://www.winemag.com/?s=&varietal=Chardonnay&drink_type=wine&page=1&search_type=reviews'
pinot_gris = 'https://www.winemag.com/?s=&varietal=Pinot%20Grigio/Gris&drink_type=wine&page=1&search_type=reviews'
sauv_blanc = 'https://www.winemag.com/?s=&varietal=Sauvignon%20Blanc&drink_type=wine&page=1&search_type=reviews'
merlot = 'https://www.winemag.com/?s=&varietal=Merlot&drink_type=wine&page=1&search_type=reviews'

wines = [cab_sauv,char,pinot_gris,sauv_blanc,merlot]

search_pages = []
for wine in wines:
    for i in range (1,25):
        search_pages.append(wine.format(i)) 


# Scrape search pages collected in previous step for links to individual wines
links = []

for page in search_pages:
    req = Request(page, headers={'User-Agent':'Mozilla/5.0'})
    webpage = urlopen(req).read()
    page_soup = soup(webpage,"html.parser")
    blocks = page_soup.findAll("a",{"class":"review-listing row"})
    sleep(randint(15,100))
    for block in blocks:
        links.append(block['href']) 


# Scrape links collected in previous step for wine name, varietal, and description
names = []
varieties = []
descriptions = []

from time import time
start_time = time()
num_requests = 0

for link in links:
'''Create request'''    
    request = requests.get(link)

'''Pause the loop'''
    sleep(randint(30,65))

'''Track progress of requests'''
    num_requests += 1
    elapsed_time = time() - start_time
    print('Request: {}; Frequency: {} requests/s'.format(num_requests, num_requests/elapsed_time))
    
'''Throw a warning for non-200 status codes'''
    if request.status_code != 200:
        warn('Request: {}; Status code: {}'.format(requests, request.status_code))

'''Create Soup'''        
    req = Request(link, headers={'User-Agent':'Mozilla/5.0'})
    webpage = urlopen(req).read()
    page_soup = soup(webpage,"html.parser")

'''Pull wine varietal'''    
    name = page_soup.find("div",{"class":"article-title"}).h1
    name.span.decompose()
    names.append(name.text)

'''Pull wine varietal'''    
    variety = page_soup.find_all("div",{"class":"info medium-9 columns"})
    varieties.append(variety[2].a.text)

'''Pull wine description'''
    description = page_soup.find("p",{"class":"description"}).text
    descriptions.append(description)


# Create dataframe with the scraped wine data
import pandas as pd

wine_data = pd.DataFrame({'name': names,
'variety': varieties,
'description': descriptions,
})

#Save as CSV for later use
wine_data.to_csv('wine_data.csv')






