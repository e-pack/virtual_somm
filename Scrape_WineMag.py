
#Inspect single wine review page to find description 

# from urllib.request import Request, urlopen
# from bs4 import BeautifulSoup as soup

# url = 'https://www.winemag.com/buying-guide/sandeman-2017-quinta-do-seixo-port/'

# req = Request(url, headers={'User-Agent':'Mozilla/5.0'})
# webpage = urlopen(req).read()

# #Define Page Soup
# page_soup = soup(webpage,"html.parser")

# #Pull all descriptions paragraphs
# description = page_soup.find("p",{"class":"description"})

# print(description.findAll(text=True))


#Define a function to scrape indibidual wine pages 
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

search_pages = []
for i in range (1,10):
    search_pages.append("https://www.winemag.com/?s=&drink_type=wine&page={}&search_type=reviews".format(i))

print(search_pages)
	
url_list = []

req = Request('https://www.winemag.com/?s=&drink_type=wine&page=6&search_type=reviews', headers={'User-Agent':'Mozilla/5.0'})
webpage = urlopen(req).read()
page_soup = soup(webpage,"html.parser")
link = page_soup.findAll("a",{"class":"review-listing row"})
#link = link.findAll(text=True)
link.append(url_list)

print(url_list)





#<a class="review-listing row" href="https://www.winemag.com/buying-guide/sandeman-2017-quinta-do-seixo-port/" data-review-id="326327">





# descriptions = []
# def scrape_description(url_list):
# 	for url in url_list:
# 		req = Request(url, headers={'User-Agent':'Mozilla/5.0'})
# 		webpage = urlopen(req).read()
# 		page_soup = soup(webpage,"html.parser")
# 		description = page_soup.find("p",{"class":"description"})
# 		description = description.findAll(text=True)
# 		descriptions.append(description)


# print()