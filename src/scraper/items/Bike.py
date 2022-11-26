from scrapy.item import Item, Field

class Bike(Item):
    # define the fields for your item here like:
    name = Field()
    manufacturer = Field()
    year= Field()
    category= Field()
    photos= Field()
    videos= Field()
    specs = Field()
    
    # name = scrapy.Field()