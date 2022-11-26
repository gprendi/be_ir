from scrapy.item import Item, Field

class Manufacturer(Item):
    bikes = Field()
    name = Field()
    reviews = Field()