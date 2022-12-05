# this is a crawler used to crawl information from a website about motorcycles

import scrapy

from src.scraper.items.Bike2 import Bike2

class MotorcycleSpider2(scrapy.Spider):
    # define a name 
    name = 'Motorcycle2'
    start_urls = ["https://www.trademe.co.nz/a/motors/motorbikes/motorbikes"]
    # parse the data
    def parse_string(self, string):
        # parse the string
        return string.encode("ascii", "ignore").decode().replace(":", "").strip()

    # fourth step, we define a function to parse the data we want
    def parse(self, response):
        print(" resp link", response.url)
        title = response.css('.tm-motors-listing__title::text').get();
        main_image = response.css('.tm-progressive-image-loader__full::attr(src)').get()
        secondary_images = response.css('.tm-gallery-view__thumbnail::attr(src)').getall()
        payment_options = response.css(".o-rack-item__secondary::text").get();
        description = response.css('.tm-markdown').getall();
        buy_now_price = response.css('.tm-buy-now-box__price strong::text').get();
        starting_price = response.css('.h-text-align-center strong::text').get();
        time_remaining = response.css('.tm-listing-close-time__remaining::text').get();
        seller_location: response.css('.tm-motors-date-city-watchlist__location::text').get();
        specs = response.css('.tm-vehicle-attributes .tm-motors-vehicle-attributes__attribute-section').get();

        yield {
            'title': title,
            'main_image': main_image,
            'secondary_images': secondary_images,
            'payment_options': payment_options,
            'description': description,
            'buy_now_price': buy_now_price,
            'starting_price': starting_price,
            'time_remaining': time_remaining,
            'seller_location': seller_location,
            'specs': specs
        }

    def parse_title(self, response):
        print("parsing title")
        title = response.css('.tm-motors-listing__title::text').get();
        print("title", title)
        yield response.follow(title, self.parse)
    

    def parse_payment_options(self, response):
        print("parsing payment options")
        payment_options = response.css(".o-rack-item__secondary::text").get();
        for payment_option in payment_options:
           print("payment_option", payment_option)
           yield response.follow(payment_option, self.parse)
        

    def parse_description(self, response):
        print("parsing description")
        description = response.css('.tm-markdown').getall();
        for desc in description:
           if (desc != None):
              if (desc != ''):
                     print("desc", desc)

        yield response.follow(desc, self.parse)
    

    def parse_specs(self, response):
        specs = response.css('.tm-vehicle-attributes .tm-motors-vehicle-attributes__attribute-section').get();
        for spec in specs:
            url = specs.css('a::attr(href)').get()
            if url is not None:
                yield response.follow(url, self.parse)
            else:
                print("spec", spec)
                yield response.follow(spec, self.parse)
    

    def parse_motorbikes_page(self, response):
        print("parsing motorbikes page")
    
        title = response.css('.tm-motors-listing__title::text').get();
        
        # parse the data
        item = Bike2()
        item['title'] = title
        item['main_image'] = response.css('.tm-progressive-image-loader__full::attr(src)').get()
        item['secondary_images'] = response.css('.tm-gallery-view__thumbnail::attr(src)').getall()
        item['payment_options'] = response.css(".o-rack-item__secondary::text").get();
        item['description'] = response.css('.tm-markdown').getall();
        item['buy_now_price'] = response.css('.tm-buy-now-box__price strong::text').get();
        item['starting_price'] = response.css('.h-text-align-center strong::text').get();
        item['time_remaining'] = response.css('.tm-listing-close-time__remaining::text').get();
        item['seller_location'] = response.css('.tm-motors-date-city-watchlist__location::text').get();
        item['specs'] = response.css('.tm-vehicle-attributes .tm-motors-vehicle-attributes__attribute-section').get();
        yield item
    

    






    




    


    











    # def parse_price(self, response):
    #     # parse the price
    #     print(" resp link", response.url)
    #     price = response.css('.tm-motors-search-card__price::text').get()
    #     print("price", price)
    #     # after parsing the price, iterate over the list of prices
    #     for prices in price:
    #         # parse the price
    #         yield response.follow(prices, self.parse)
    
    # def parse_brand(self, response):
    #     print("link", response.url)
    #     bikes = response.css('.tm-motors-search-card__title::text').getall()
    #     print(" bikes ", bikes)
    #     for bike in bikes:
    #         yield response.follow(bike, self.parse_bike_page2)
    #     next_page = response.css('.o-pagination__link').get()
    #     print("next page::", next_page)
    #     for page in next_page:
    #         yield response.follow(page, self.parse_brand)
    
    # def parse_bike_page2(self, response):
    #     print("urlrlrlrlrll", response.url)
    #     city = response.css('.tm-motors-search-card__location').get()
    #     price = response.css('.tm-motors-search-card__price::text').get()
    #     cc = response.css('.tm-motors-search-card__engine-details::text').get()
    #     kms = response.css('.tm-motors-search-card__body-odometer::text').get()
    #     list_date = response.css('.tm-motors-closing-time__font-weight::text').get()
    #     road_costs_included = response.css('.tm-motors-search-card__on-road-costs::text').get()
    #     brand = response.css('.tm-motors-search-card__title::text').get()
    #     # parse the item
    #     item = Bike2()
    #     item['city'] = city
    #     item['price'] = price
    #     item['cc'] = cc
    #     item['kms'] = kms
    #     item['list_date'] = list_date
    #     item['road_costs_included'] = road_costs_included
    #     item['brand'] = brand
    #     yield item
    #     # parse the next page
    #     next_page = response.css('.o-pagination__link').get()
    #     print("next page::", next_page)
    #     for page in next_page:
    #         yield response.follow(page, self.parse_bike_page2)
        
    
    # def parse_cc(self, response):
    #     print("parsing cc")
    #     cc = response.css('.tm-motors-search-card__engine-details::text').get()
    #     print("cc", cc)
    #     for ccs in cc:
    #         print("css", ccs)
    #         yield response.follow(ccs, self.parse)
    #     next_page = response.css('.o-pagination__link').get()
    #     print("next page::", next_page)
    #     for page in next_page:
    #         yield response.follow(page, self.parse_cc)
        
    # def parse_kms(self, response):
    #     print("parsing kms")
    #     kms = response.css('.tm-motors-search-card__body-odometer::text').get()
    #     print("kms", kms)
    #     for kmss in kms:
    #         yield response.follow(kmss, self.parse)
    #     next_page = response.css('.o-pagination__link').get()
    #     print("next page::", next_page)
    #     for page in next_page:
    #         yield response.follow(page, self.parse_kms)
    
    # def parse_list_date(self, response):
    #     print("parsing list date")
    #     list_date = response.css('.tm-motors-closing-time__font-weight::text').get()
    #     print("list date", list_date)
    #     for list_dates in list_date:
    #         yield response.follow(list_dates, self.parse)
    #     next_page = response.css('.o-pagination__link').get()
    #     print("next page::", next_page)
    #     for page in next_page:
    #         yield response.follow(page, self.parse_list_date)
    
    # def parse_road_costs_included(self, response):
    #     print("parsing road costs included")
    #     road_costs_included = response.css('.tm-motors-search-card__on-road-costs::text').get()
    #     print("road costs included", road_costs_included)
    #     for road_costs_includeds in road_costs_included:
    #         yield response.follow(road_costs_includeds, self.parse)
    #     next_page = response.css('.o-pagination__link').get()
    #     print("next page::", next_page)
    #     for page in next_page:
    #         yield response.follow(page, self.parse_road_costs_included)

    
        
        

    
        
    

        
    
        

    
        
        



