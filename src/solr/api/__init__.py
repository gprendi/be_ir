import requests
import json

class api:
    
    def __init__(self, solr_host):
        self.host = solr_host;

    
    def index(self, filepath, collection):
        pass 
    
    def read_configfile(self, configfile_path):
        
        with open(configfile_path) as configfile:
            obj = json.load(configfile)
            
            return obj['config']
    
    def read_schemafile(self, schemafile_path):
        with open(schemafile_path) as schemafile:
            obj = json.load(schemafile)

            fields =  obj['schema']['fields']
            cpyfields = obj['schema']['copy-fields']
            data = '{'
            for field in fields:
            
                data = data + "'add-field':" + field.__str__() + ","
            
            for cpyfield in cpyfields:
                data = data + "'add-copy-field':" + cpyfield.__str__() + ","
            data = data + '}'
            return data 
        
    
    def index_docs(self, collection, docs):
        q = f'{self.host}/api/collections/{collection}/update?commit=true'
        
        try:
            
            print(docs)
            jdata = json.dumps(docs)
            resp = requests.post(q, data=jdata, headers={'Content-Type': 'application/json'})
            print(resp)
            print(resp.json())
            return resp.json()
        except:
            return { "error": True}
    
    def delete_collection(self, collectioname):
        q = f'{self.host}/solr/admin/collections?action=DELETE&name={collectioname}'
        
        try:
            resp = requests.get(q)
            return resp.json()
        except:
            return {"error" :True}
    
    def create_collection(self, collectioname):
        q = f'{self.host}/solr/admin/collections?action=CREATE&name={collectioname}&numShards=3&replicationFactor=2&wt=json'
        try:
            resp = requests.get(q)
            return resp.json()
        except:
            return { "error": True}
        
    def create_alias(collection):
        pass
    
    def change_cores(collection):
        pass
    
    def update_schema(self, collection, schema_updates):
        q = f'{self.host}/api/collections/{collection}/schema'
        
        try:
            resp = requests.post(q, data=schema_updates, headers={'Content-Type': 'application/json'})
            return resp.json()
        except:
            return { "error": True}
       
    
    def update_config(self, collection, config_updates):
        q = f'{self.host}/api/collections/{collection}/config'
        
        try:
            jdata = json.dumps(config_updates)
            resp = requests.post(q, data=jdata, headers={'Content-Type': 'application/json'})
            return resp.json()
        except:
            return { "error": True}
        
    
    def query(self, collection, queryterm):
        q = f'{self.host}/api/collections/{collection}/select?df=__text__&indent=true&q.op=OR&q={queryterm}&wt=json'
        
        try:
            resp = requests.get(q).json()['response']
           
            docs = resp['docs']
            return docs
        except:
            return []  
    
    def suggest(self, collection, suggestionterm):
        q = f'{self.host}/api/collections/{collection}/suggest?suggest=true&suggest.build=false&suggest.dictionary=mySuggester&wt=json&suggest.q={suggestionterm}'
        
        try:
            resp = requests.get(q).json() 
            suggestions = [x['term'] for x in resp['suggest']['mySuggester'][suggestionterm]['suggestions']]
            return suggestions
        except:
            return []
        
    def build_suggester(self, collection, suggesterName):
        
        q = f'{self.host}/api/collections/{collection}/suggest?suggest=true&suggest.build=true&suggest.dictionary={suggesterName}&wt=json&suggest.q=""'
        
        try:
            resp = requests.get(q).json()
            
            return resp
        except:
            return {'error' : True}