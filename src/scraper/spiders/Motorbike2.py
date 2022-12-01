# this is a crawler used to crawl information from a website about motorcycles

import scrapy

from scraper.items.Bike2 import Bike2

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

        # following 2 not working properly
        description = response.css('.tm-motors-listing-description p::text').getall();
        specs = response.css('.l-container .tm-vehicle-attributes::text').get();

        price = response.css('.tm-motors-pricing-box__price::text').get();
        seller_location: response.css('.tm-motors-date-city-watchlist__location::text').get();
        posted: response.css('.tm-motors-date-city-watchlist__date::text').get();

        yield {
            'title': title,
            'main_image': main_image,
            'secondary_images': secondary_images,
            'payment_options': payment_options,
            'description': description,
            'price': price,
            'seller_location': seller_location,
            'specs': specs,
            'posted': posted
        }

    def parse_description(self, response):
        # we will parse the description of each motorcycle
        title = response.css('.tm-motors-listing__title::text').get();
        specs = response.css('.l-container .tm-vehicle-attributes::text').getall();
        print(" the title is:", title)
        print(" with specs:", specs)
        for spec in specs:
            print(" spec:", spec)
        yield {
            'title': title,
            'specs': specs
        }


    def parse_price(self, response):
        # we will parse the price of each motorcycle
        title = response.css('.tm-motors-listing__title::text').get();
        price = response.css('.tm-motors-pricing-box__price::text').get();
        print(" the title is:", title)
        print(" with price:", price)
        yield {
            'title': title,
            'price': price
        }
    

    def parse_bike_page(self, response):
        print("urlrlrlrlrll", response.url)
        title = response.css('.tm-motors-listing__title::text').get();
        main_image = response.css('.tm-progressive-image-loader__full::attr(src)').get()
        secondary_images = response.css('.tm-gallery-view__thumbnail::attr(src)').getall()
        payment_options = response.css(".o-rack-item__secondary::text").get();
        description = response.css('.tm-motors-listing-description p::text').getall();
        specs = response.css('.l-container .tm-vehicle-attributes::text').get();
        price = response.css('.tm-motors-pricing-box__price::text').get();
        seller_location = response.css('.tm-motors-date-city-watchlist__location::text').get();
        posted = response.css('.tm-motors-date-city-watchlist__date::text').get();

        item = Bike2()
        item['title'] = title
        item['main_image'] = main_image
        item['secondary_images'] = secondary_images
        item['payment_options'] = payment_options
        item['description'] = description
        item['specs'] = specs
        item['price'] = price
        item['seller_location'] = seller_location
        item['posted'] = posted
        yield item
        # parse the next page
        next_page = response.css('.o-pagination__link').get()
        print("next page::", next_page)
        for page in next_page:
            yield response.follow(page, self.parse_bike_page)
        
    
    