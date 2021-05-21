import scrapy


class ShoeSpider(scrapy.Spider):
    name = 'shoes'
 
 
 #2012


start_urls = ['https://web.archive.org/web/20120704035744/http://store.nike.com/us/en_us/?l=shop,pwp,c-1+100701/hf-10002+12001+50144/t-Men%27s_Shoes']

    def parse(self, response):
        for products in response.css('div.grid-item'):
            yield{
                'name': products.css('p.griditem-display-name::text').get().replace('iD\n','').replace('\t\t',''),
                'price': products.css('span.local::text').get().replace('$',''),

            }



"""
#2013
"""



"""

 start_urls = ['https://web.archive.org/web/20130629025923if_/http://store.nike.com/us/en_us/pw/']

    def parse(self, response):
        for products in response.css('div.grid-item'):
            yield{
                'name': products.css('p.griditem-display-name::text').get().replace('iD\n','').replace('\t\t',''),
                'price': products.css('span.local::text').get().replace('$',''),

            }


"""
#2014
"""


start_urls = ['https://web.archive.org/web/20140223034104if_/http://store.nike.com/us/en_us/pw/shoes/brk']

    def parse(self, response):
        for products in response.css('div.grid-item'):
            yield{
                'name': products.css('p.griditem-display-name::text').get().replace('iD\n','').replace('\t\t',''),
                'price': products.css('span.local::text').get().replace('$',''),

            }
"""
# 2015

"""




   start_urls = ['https://web.archive.org/web/20150408161543if_/http://store.nike.com/us/en_us/pw/mens-shoes/7puZbrk']

    def parse(self, response):
        for products in response.css('div.grid-item'):
            yield{
                'name': products.css('p.product-display-name::text').get().replace('iD\n','').replace('\t\t',''),
                'price': products.css('span.local::text').get().replace('$',''),

            }


"""
#2016
"""

 start_urls = ['https://web.archive.org/web/20160806015038if_/http://store.nike.com/us/en_us/pw/mens-shoes/7puZoi3']

    def parse(self, response):
        for products in response.css('div.grid-item'):
            yield{
                'name': products.css('p.product-display-name::text').get().replace('iD\n','').replace('\t\t',''),
                'price': products.css('span.local::text').get().replace('$',''),

            }

"""
#2017
"""
start_urls = ['https://web.archive.org/web/20170925012126if_/https://store.nike.com/us/en_us/pw/mens-shoes/7puZoi3']

    def parse(self, response):
        for products in response.css('div.grid-item'):
            yield{
                'name': products.css('p.product-display-name::text').get().replace('iD\n','').replace('\t\t',''),
                'price': products.css('span.local::text').get().replace('$',''),

            }

"""
2018

"""

start_urls = ['https://web.archive.org/web/20180927020453if_/https://store.nike.com/us/en_us/pw/mens-shoes/7puZoi3']

    def parse(self, response):
        for products in response.css('div.grid-item'):
            yield{
                'name': products.css('p.product-display-name::text').get().replace('iD\n','').replace('\t\t',''),
                'price': products.css('span.local::text').get().replace('$',''),

      
            }
"""


"""
#2019



start_urls = ['https://web.archive.org/web/20190331040349/https://store.nike.com/us/en_us/pw/mens-shoes/7puZoi3']

    def parse(self, response):
        for products in response.css('div.grid-item'):
            yield{
                'name': products.css('p.product-display-name::text').get().replace('iD\n','').replace('\t\t',''),
                'price': products.css('span.local::text').get().replace('$',''),

            }

"""
"""

2020

start_urls = ['https://web.archive.org/web/20200331045809if_/https://www.nike.com/w/mens-shoes-nik1zy7ok']

    def parse(self, response):
        for products in response.css('div.product-card'):
            yield{
                'name': products.css('div.product-card__title::text').get().replace('iD\n','').replace('\t\t',''),
                'price': products.css('div.css-b9fpep::text').get().replace('$',''),

            }




2021


"""
"""
import scrapy


class ShoeSpider(scrapy.Spider):
    name = 'shoes'
    start_urls = ['https://www.nike.com/ca/w/new-mens-shoes-3n82yznik1zy7ok']

    def parse(self, response):
        for products in response.css('div.product-card__info'):
            yield{
                'name': products.css('div.product-card__title::text').get() ,
                'price': products.css('div.product-price::text').get().replace('$',''),


"""