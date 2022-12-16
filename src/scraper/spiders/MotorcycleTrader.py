import scrapy


class MotorcycleSpider(scrapy.Spider):
    name = 'MotorcycleTrader'
    start_urls = ["https://www.mototrader.ch/occasion-neu-oldtimer-privat-export-racing-motorrad/resultateliste/kategorie:alle/marke:alle/modell:alle/fzart:1,2,3,4,5,0,7/hubraum:alle/kmstand:alle/jahr:min-max/preis:alle/1-100-1-sort99"]
    base_link = "https://www.mototrader.ch"
    def parse_single_listing(self, response):
        
        details_divs = response.css(".DetailDiv")
        
        images = []
        desc = []
        if len(details_divs) > 0:
            images = details_divs[0].css("img::attr('src')").getall()
        if len(details_divs) > 1:
            desc = details_divs[1].css("span::text").getall()
        # detaildesc = response.css(".DetailDesc")[0]

        # key = detaildesc.css(".leftside-detail-text::text").getall()
        # value = detaildesc.css(".rightside-detail-text::text").getall()
        
        item = {
            "images": images,
            "link": response.url,
            "desc": desc    
        }
        
        
        yield item
    
    
    def parse(self, response):
        
        all_listings = response.css(".ListeField::attr('attrid')").getall()
        
        for listing in all_listings:
            link = self.base_link + listing
            yield response.follow(link, self.parse_single_listing)        
        
        page_numbers = []
        if len(response.css(".pagerNumbersNew")) > 0:
            page_numbers = response.css(".pagerNumbersNew")[1].css("a")
        
        print(len(page_numbers))
        current = -1
        i = 0
        for page_ref in page_numbers:
            print("hello " + page_ref.css("a::attr('href')").get() )
            if "javascript:void(0);" in page_ref.css("a::attr('href')").get():
                current = i
                break
            i += 1
            
        if current == len(page_numbers) - 1:
            current = -1
        
        if current > -1:
            print(" hey there ")
            next_page = self.base_link + page_numbers[current + 1].css("a::attr('href')").get()
            if next_page is not None:
                print(" hey there2 ")
                yield response.follow(next_page, self.parse)