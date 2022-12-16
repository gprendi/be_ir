import json
import requests

def index(filepath, collection, host):
    
    q = f'/api/collections/{collection}/update'
    with open(filepath) as docsfile:
        docs = json.load(docsfile)
        
        resp = requests.post(q, data=docs, headers={'Content-Type': 'application/json'})
        
        print(resp.json())
        


def create_alias():
    pass 
