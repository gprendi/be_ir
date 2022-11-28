# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scraper.items.Bike import Bike

def toInt(str):
    try:
        return int(str) 
    except ValueError:        
        try:
            return float(str)
        except ValueError:
            return None

class ScraperPipeline:
    def process_item(self, item, spider):
        # flatten items
        
        item2 = ItemAdapter(item)
        if not item2.is_item(Bike):
            return item
        
        item_ = {}
        
        bikeItem = Bike(item)
        specs = item['specs']
        item_['name'] = bikeItem['name']
        item_['manufacturer'] = bikeItem['manufacturer']
        item_['year']= toInt(bikeItem['year'])
        
        for k in specs.keys():
            obj = specs[k]
            for key in obj.keys():
                intVal = toInt(obj[key])
                if (intVal is not None):
                    item_[key] = intVal
                else:
                    item_[key] = obj[key]
        
        return item_

class ScraperPipeline2:
    def process_item(self, item, spider):
        return item
