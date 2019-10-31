from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'https://www.giftrocker.com/secure/reservationtables/?c=fedc33dc'

#Open up connection and add page
uClient = uReq(my_url)

#Pull html into variable and close read
page_html = uClient.read()
uClient.close()

#Define Page Soup
page_soup = soup(page_html,"html.parser")

#Pull all reservations blocks that are open
open_res_blocks = page_soup.findAll("input",{"class":"res-event-table res-event-open-table"})

#Define the nunber of reservations
number_of_reservations = len(open_res_blocks)

print(len(open_res_blocks))
