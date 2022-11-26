# this is a crawler used to crawl information from a website about motorcycles

import scrapy

from scraper.items.Bike2 import Bike2

class MotorcycleSpider2(scrapy.spider):
    # define a name 
    name = 'Motorcycle2'
    start_urls = ["https://www.trademe.co.nz/a/motors/motorbikes/motorbikes"]
    # parse the data
    def parse_string(self, string):
        # parse the string
        return string.encode("ascii", "ignore").decode().replace(":", "").strip()

    # fourth step, we define a function to parse the data we want
    def parse2(self, response):
        # parse the bike page
        print(" resp link", response.url)
        # parse the city: css -> tmid="location"
        city = response.css('.tm-motors-search-card__location').get()
        price = response.css('.tm-motors-search-card__price::text').get()
        cc = response.css('.tm-motors-search-card__engine-details::text').get()
        kms = response.css('.tm-motors-search-card__body-odometer::text').get()
        list_date = response.css('.tm-motors-closing-time__font-weight::text').get()
        road_costs_included = response.css('.tm-motors-search-card__on-road-costs::text').get()
        brand = response.css('.tm-motors-search-card__title::text').get()

    

    def parse_price(self, response):
        # parse the price
        print(" resp link", response.url)
        price = response.css('.tm-motors-search-card__price::text').get()
        print("price", price)
        # after parsing the price, iterate over the list of prices
        for prices in price:
            # parse the price
            yield response.follow(prices, self.parse2)
    
    def parse_brand(self, response):
        print("link", response.url)
        bikes = response.css('.tm-motors-search-card__title::text').getall()
        print(" bikes ", bikes)
        for bike in bikes:
            yield response.follow(bike, self.parse_bike_page2)
        next_page = response.css('.o-pagination__link').get()
        print("next page::", next_page)
        for page in next_page:
            yield response.follow(page, self.parse_brand)
    
    def parse_bike_page2(self, response):
        print("urlrlrlrlrll", response.url)
        city = response.css('.tm-motors-search-card__location').get()
        price = response.css('.tm-motors-search-card__price::text').get()
        cc = response.css('.tm-motors-search-card__engine-details::text').get()
        kms = response.css('.tm-motors-search-card__body-odometer::text').get()
        list_date = response.css('.tm-motors-closing-time__font-weight::text').get()
        road_costs_included = response.css('.tm-motors-search-card__on-road-costs::text').get()
        brand = response.css('.tm-motors-search-card__title::text').get()
        # parse the item
        item = Bike2()
        item['city'] = city
        item['price'] = price
        item['cc'] = cc
        item['kms'] = kms
        item['list_date'] = list_date
        item['road_costs_included'] = road_costs_included
        item['brand'] = brand
        yield item
        # parse the next page
        next_page = response.css('.o-pagination__link').get()
        print("next page::", next_page)
        for page in next_page:
            yield response.follow(page, self.parse_bike_page2)
        
    
    def parse_cc(self, response):
        print("parsing cc")
        cc = response.css('.tm-motors-search-card__engine-details::text').get()
        print("cc", cc)
        for ccs in cc:
            yield response.follow(ccs, self.parse2)
        next_page = response.css('.o-pagination__link').get()
        print("next page::", next_page)
        for page in next_page:
            yield response.follow(page, self.parse_cc)
        
    def parse_kms(self, response):
        print("parsing kms")
        kms = response.css('.tm-motors-search-card__body-odometer::text').get()
        print("kms", kms)
        for kmss in kms:
            yield response.follow(kmss, self.parse2)
        next_page = response.css('.o-pagination__link').get()
        print("next page::", next_page)
        for page in next_page:
            yield response.follow(page, self.parse_kms)
    
    def parse_list_date(self, response):
        print("parsing list date")
        list_date = response.css('.tm-motors-closing-time__font-weight::text').get()
        print("list date", list_date)
        for list_dates in list_date:
            yield response.follow(list_dates, self.parse2)
        next_page = response.css('.o-pagination__link').get()
        print("next page::", next_page)
        for page in next_page:
            yield response.follow(page, self.parse_list_date)
    
    def parse_road_costs_included(self, response):
        print("parsing road costs included")
        road_costs_included = response.css('.tm-motors-search-card__on-road-costs::text').get()
        print("road costs included", road_costs_included)
        for road_costs_includeds in road_costs_included:
            yield response.follow(road_costs_includeds, self.parse2)
        next_page = response.css('.o-pagination__link').get()
        print("next page::", next_page)
        for page in next_page:
            yield response.follow(page, self.parse_road_costs_included)

    
        
        

    
        
    

        
    
        

    
        
        



