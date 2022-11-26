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
        q = f'http://localhost:8983/solr/motorcycles__/select?df=__text__&indent=true&q.op=OR&q={search}&wt=json&fl=name,year,manufacturer'
        
        resp = requests.get(q).json()['response']

        docs = resp['docs']
        
        return docs
    return app