import json
import pymongo
from pymongo import MongoClient
import tleutils as tu

#Default MongoDB client
defclient = MongoClient("mongodb+srv://ljmendel:LinkBudget360@linkdata.mvf2x.mongodb.net/Link%95Budget?retryWrites=true&w=majority")

def write2db(inputjson, inputtle = 0, client = defclient, db = "SDProject", collect = "LinkData"):
    db = client[db]
    collection = db[collect]
    
    if inputtle != 0:
        tu.tle2json(inputtle, "temp.json")
        tu.mergejson("temp.json", inputjson)
    
    f = open(inputjson)
    data = json.load(f)
    
    if isinstance(data,list):
        collection.insert_many(data)
    else:
        collection.insert_one(data)
    
    #collection.delete_many({})
    f.close()
