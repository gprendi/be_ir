from flask import Flask
from flask import request
from os import path
import requests
from src.solr.api import api as solrapi
import os 
import atexit
import asyncio
from multiprocessing import Process
from flask_apscheduler import APScheduler
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from src.scraper.spiders.MotorcycleSpider import MotorcycleSpider
import json
from threading import Thread
settings = get_project_settings()

host = os.environ.get('HOST') or "http://localhost:8983"
collection = os.environ.get('COLLECTION') or "motorcycles"


def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()

def define_app():
    app = Flask(__name__)
    api = initApi()
    process = initCrawlingProcess(api)
    
    
    scheduler = APScheduler()
    scheduler.init_app(app)
    
    
    @scheduler.task('interval', id='scrape', minutes=60)
    def scrape():
        def run_crawl():
            
            crawl_process = CrawlerProcess(settings)
            
            
            crawl_process.crawl(MotorcycleSpider)
            crawl_process.start()

        get_or_create_eventloop()
        
        process = Process(target=run_crawl)
        process.start()
        process.join()

        print("suggester after scraping", api.build_suggester(collection, "mySuggester"))
        print("finished")
    
    scheduler.start()
    
    @app.get("/")
    def hello_world():
        return 'Hello World'

    @app.get("/hell")
    def hi():
        return "hi"

    @app.get("/query")
    def query():
        search = request.args.get("query")
        
        return api.query(collection=collection, queryterm=search)

    @app.get("/recommend")
    def recommend():
        suggest = request.args.get("suggest")
        
        return api.suggest(collection=collection, suggestionterm=suggest)
    
    
    return app

def initApi() -> solrapi:
    
    api = solrapi(host)
    print(api.delete_collection(collectioname=collection))
    print(api.create_collection(collectioname=collection))
    
    schema_updates = api.read_schemafile("./src/solr/schema.json")
    config_updates = api.read_configfile("./src/solr/config.json")
    
    
    
    print("config ", config_updates)    
    res = api.update_schema(collection=collection, schema_updates=schema_updates)
    
    if (res.get('error')):
        print(" schema wrong")
        pass # sys.env 1
    
    res = api.update_config(collection=collection, config_updates=config_updates)
    print("res ", res)
    if (res.get('error')):
        print(" config wrong 0")         
        pass # sys.env 1
    
    with open("./data/motorcycles.json") as file:
        obj = json.load(file)
        api.index_docs(collection=collection, docs =obj)
    print("suggester build", api.build_suggester(collection=collection, suggesterName="mySuggester"))
    
    return api 

def initCrawlingProcess(api, ) -> CrawlerProcess:
    process = CrawlerProcess(settings)
    process.crawl(MotorcycleSpider)
    
    return process    



