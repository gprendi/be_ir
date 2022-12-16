import scrapy

from src.scraper.items.Bike import Bike

class MotorcycleSpider(scrapy.Spider):
    name = 'Motorcycle'
    start_urls = ["https://www.motorcycle.com"]
    
    def parse_string(self, string):
        return string.encode("ascii", "ignore").decode().replace(":", "").strip()
    
    
    def parse_bike_page(self, response):
        sub_buttons = response.css(".submit a")
        next_resp = None
        if len(sub_buttons) == 4:
            next_resp = response.css(".submit a")[2].css("a::attr(href)").get()
        if next_resp is not None and "detail" in next_resp:
            # fetch details
            yield response.follow(next_resp, self.parse_bike_page)

        # parse details
        name = response.css('.intro h2::text').get()
        item = Bike()
        item['name'] = name
        spl = name.split()
        item['year'] = spl[0]
        item['manufacturer'] = spl[1]
        item['link'] = response.url
        item['main'] = True
        
        specs = {}
        
        obj = None
        rows = response.css(".table_info tr")
        for row in rows:
            isTableHeader = len(row.css("th")) != 0
            if isTableHeader:
                obj = self.parse_string(row.css("th strong::text").get())
                if specs.get(obj) == None:
                    specs[obj] = {}
            if not isTableHeader and obj is not None:
                td = row.css("td::text").getall()
                if len(td) == 2:
                    key = self.parse_string(td[0])
                    val = self.parse_string(td[1])
                    specs[obj][key] = val
        
        item['specs'] = specs
        yield item
        
        
    def parse_manufacturer(self, response):
        bikes = response.css(".feature h2 a::attr(href)").getall()
        for bike in bikes:
            
            yield response.follow(bike, self.parse_bike_page)
            
        next_page = response.css(".next::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse_manufacturer)     
        
    
    def parse_specs(self, response):
        
        manifacturer_list = response.css(".manufacturer_list a")
        
        for manufacterer in manifacturer_list:
            url = manufacterer.css("a::text").get()
            yield response.follow(url, self.parse_manufacturer)
        
    
    def parse(self, response):
        brandsList = response.css("#brands-list li a::attr(href)").getall()
        categoryList = response.css(".category-list li a::attr(href)").getall()
        
        classifieds = response.css(".Classifieds a::attr(href)").get()
        specs = response.css(".Specs a::attr(href)").get()
      
        bikeReviews = response.css(".Bike-Reviews a::attr(href)").get()
        news = response.css(".News a::attr(href)").get()
        videos = response.css(".Videos a::attr(href)").get()
        top10 = response.css(".Top-10 a::attr(href)").get()
        insurance = response.css(".Insurance a::attr(href)").get()
        
        

        yield response.follow(specs, self.parse_specs) 
        

        