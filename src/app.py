from flask import Flask
from flask import request
import requests

def define_app():
    app = Flask(__name__)

    @app.get("/")
    def hello_world():
        return 'Hello World'

    @app.get("/hell")
    def hi():
        return "hi"

    @app.get("/query")
    def query():
        search = request.args.get("query")
        q = f'http://localhost:8983/solr/motorcycles4/select?df=__text__&indent=true&q.op=OR&q={search}&wt=json&fl=name,year,manufacturer'
        
        resp = requests.get(q).json()['response']

        docs = resp['docs']
        
        return docs
    
    @app.get("/recommend")
    def recommend():
        suggest = request.args.get("suggest")
        
        q =  f'http://localhost:8983/solr/motorcycles4/suggest?suggest=true&suggest.build=false&suggest.dictionary=mySuggester&wt=json&suggest.q={suggest}'
        resp = requests.get(q).json()
        print(" resp ", resp)
        suggestions = [x['term'] for x in resp['suggest']['mySuggester'][suggest]['suggestions']]
        print( suggestions );
        return suggestions
    return app