# -*- coding: utf-8 -*-
import scrapy

cab_sauv = 'https://www.winemag.com/?s=&varietal=Cabernet%20Sauvignon&drink_type=wine&page={}&search_type=reviews'
char = 'https://www.winemag.com/?s=&varietal=Chardonnay&drink_type=wine&page={}&search_type=reviews'
pinot_gris = 'https://www.winemag.com/?s=&varietal=Pinot%20Grigio/Gris&drink_type=wine&page={}&search_type=reviews'
sauv_blanc = 'https://www.winemag.com/?s=&varietal=Sauvignon%20Blanc&drink_type=wine&page={}&search_type=reviews'
merlot = 'https://www.winemag.com/?s=&varietal=Merlot&drink_type=wine&page={}&search_type=reviews'

wines = [cab_sauv,char,pinot_gris,sauv_blanc,merlot]

search_pages = []
for wine in wines:
    for i in range (1,75):
        search_pages.append(wine.format(i)) 

class WinebotSpider(scrapy.Spider):
    name = 'winebot'
    allowed_domains = ['winemag.com']
    start_urls = search_pages

    def parse(self,response):
    	urls_follow = [] #Used to collect all the links first
    	
    	for link in response.css(".review-listing::attr(href)").getall():
    		url = response.urljoin(link)
    		urls_follow.append(url)

    	for url in urls_follow:
    		yield scrapy.Request(url, callback=self.scrape_info)

    def scrape_info(self, response):

        print("procesing:"+response.url)
        #Extract data using css selectors
        product_name=response.css('.title::text').getall()
        variety=response.xpath('//div[@class="info medium-9 columns"]/span/a[contains(@href,"varietal")]/text()').getall()
        description = response.xpath('//p[@class="description"]/text()').getall() 
        
        row_data=zip(product_name,variety,description)

        #Making extracted data row wise
        for item in row_data:
            #create a dictionary to store the scraped info
            scraped_info = {
                #key:value
                'page':response.url,
                'product_name' : item[0], #item[0] means product in the list and so on, index tells what value to assign
                'variety' : item[1],
                'description' : item[2],
            }

            #yield or give the scraped info to scrapy
            yield scraped_info



















 

