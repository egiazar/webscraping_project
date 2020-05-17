from scrapy import Spider, Request
from squaremeal.items import SquaremealItem
import re
import math
import numpy as np




class SquaremealSpider(Spider):
    name = 'squaremeal_spider'
    allowed_urls = ['https://www.squaremeal.co.uk/']
    start_urls = ['https://www.squaremeal.co.uk/restaurants/london/local-restaurants']


    def parse(self, response):

        resto_total = response.xpath('//div[@class="col-lg-8 text-lg-center"]/h1/span/text()').extract()


        resto_total = ' '.join(resto_total).split()[0]

        num_of_pages = np.int(resto_total) // 15
        




        result_urls = ['https://www.squaremeal.co.uk/restaurants/london/local-restaurants?page={}'.format(x) for x in range (1, num_of_pages+1)]




      
        for url in result_urls:

            yield Request(url=url, callback=self.parse_result_page)


    def parse_result_page(self, response):
        
        temp_urls = response.xpath('//div[@class="result my-4"]//a/@href').extract() 
        resto_urls = list(set(temp_urls)) 
        resto_urls = [f'https://www.squaremeal.co.uk{url}' for url in resto_urls]


   



        for url in resto_urls:
            yield Request(url=url, callback=self.parse_resto_page)

        




    def parse_resto_page(self, response):

        name = response.xpath('//div[@class="row"]//h1/text()').extract()


        try:
            cuisine = response.xpath('//div[@class="mb-1 mb-md-2"]/div[3]/div[2]/text()').extract()[1]

            

        except IndexError:

            cuisine = response.xpath('//div[@class="d-inline-block mr-3"]//text()').extract()[1] 

        cuisine = cuisine.replace('\r\n', '').rstrip()  






        try:
            avg_price = response.xpath('//*[@id="overview"]/div/div[2]/div/div[1]/text()').extract()  

            avg_price = avg_price[2].strip()

            avg_price = re.findall(r'\d+', avg_price)

            price =np.mean(list(np.float_(avg_price)))

        except IndexError:
            price = 'N\A'









#number of reviews
        try:

            num_reviews = response.xpath('//div[@class="d-inline-block mr-3 mr-md-4 reviews"]/a//text()').extract()    

            num_reviews = np.int(' '.join(num_reviews).split()[0]) 

        except IndexError:
            num_reviews = 0



#number of stars(rating)

        try:


            ratings = response.xpath('//div[@class="d-inline-block mr-3 mr-md-4 reviews"]/a//span').extract()

            stars = 5

            for el in reversed(ratings):
                if ('o' in el and 'half' not in el):
                    stars = stars -1
                elif ('half' in el):
                    stars = stars - 0.5

        except:
            stars = 0

        

    







           




        item = SquaremealItem()
        item['name'] = name
        item['cuisine'] = cuisine
        item['price'] = price
        item['num_reviews'] = num_reviews
        item['stars']  = stars   

        yield item








