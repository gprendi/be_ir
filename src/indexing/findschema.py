import json

specs = {
    "Engine": {},
    "Transmission": {},
    "Wheels & Tires": {},
    "Brakes": {},
    "Technical Specifications": {},
    "Identification": {}
}
schema = {
    "name": "2022 BMW R 1250 GS",
    "year": "2022",
    "manufacturer": "BMW",
    "specs": specs
}

with open("../motorcycles.json") as file:
    allObj = json.load(file)
    for obj in allObj:
        # specs obj
        spec = obj['specs']
        for key in spec.keys():
            # print(key, '--')
            spObj = spec[key]
            for k in spObj.keys():=
                # print(k)
                if (specs[key].get(k) == None):
                    specs[key][k] = ""  
      
        
        # print("obj ", obj)

with open("schema.json", 'w') as file:
    json.dump(schema, file)