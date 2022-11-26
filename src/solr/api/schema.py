import json
import requests

with open("../schema.json") as schemafile:
    obj = json.load(schemafile)

    fields =  obj['schema']['fields']
    cpyfields = obj['schema']['copy-fields']
    data = '{'
    for field in fields:
        print ("field ",field.__str__() )
        data = data + "'add-field':" + field.__str__() + ","
    
    for cpyfield in cpyfields:
        data = data + "'add-copy-field':" + cpyfield.__str__() + ","
    data = data + '}'
    # data = json.dumps(data)
    # print(data)
    resp = requests.post("http://localhost:8983/api/collections/motorcycles__/schema", data=data, headers={'Content-Type': 'application/json'})
    
    print("response", resp)
    print(resp.json())