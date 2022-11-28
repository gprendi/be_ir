from scrapy.item import Item, Field

class Bike2(Item):
    # define the fields for your item:
    city = Field()
    price = Field()
    cc = Field()
    kms = Field()
    list_date = Field()
    road_costs_included = Field()
    brand = Field()
    
   






