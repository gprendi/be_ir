# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from src.scraper.items.Bike import Bike
from src.solr.api import api as solrapi
import os

host = os.environ.get('HOST') or "http://localhost:8983"

collection = os.environ.get('COLLECTION') or "motorcycles"
counter = 0
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
        
        # if not item2.is_item(Bike):
        #     return item
        
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

class SolrScraperPipeline:
    
    def __init__(self) -> None:
        self.api = solrapi(host)
        
    def process_item(self, item, spider):
        print(self.api.index_docs(collection, item))
        
        return item
