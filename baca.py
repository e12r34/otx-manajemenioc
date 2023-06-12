import pymongo, json, os, random, string
import json

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["db_manajemen_ioc"]
coll = mydb["cl_pulse"]

a=open("file1.json","r")
stringnya=a.read()

a.close()

jsonnya=json.loads(stringnya)
# print(jsonnya['count'])
# print(len(jsonnya['results']))
res=coll.find({'tags':'trojan'})
for i in res:
    print(i)
    print()