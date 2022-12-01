from scrapy.item import Item, Field

class Bike2(Item):
    # define the fields for your item:
    title = Field()
    main_image = Field()
    secondary_images = Field()
    payment_options = Field()
    description = Field()
    specs = Field()
    price = Field()
    seller_location = Field()
    posted = Field()


    
   






