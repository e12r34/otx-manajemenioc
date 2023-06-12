#Codingan ini buat ngecek apakah modified datenya udah lebih dari sebulan, kalau udah lebih dari sebulan, dia otomatis didisable
from datetime import datetime, timedelta
import pymongo
from custom_logging import make_log

file_log=open("log_operation.log","a")
# connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["db_manajemen_ioc"]
collection = db["cl_pulse"]
collection_ioc=db["cl_ioc"]

# define the threshold for the modified date
threshold = datetime.now() - timedelta(days=30)

# find the documents that have a modified date before the threshold
query = {"modified": {"$lt": threshold.strftime("%Y-%m-%dT%H:%M:%S.%f")}}
documents = collection.find(query,{"id":1})

# loop through the documents and update or create new data
for document in documents:
    # do something here, e.g. update or insert new data
    filter = {'otx_id': document['id']}
    update = {'$set': {'status': False}}
    try:
        operation=collection_ioc.update_many(filter,update)
        now=datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        if operation.modified_count > 0:
            make_log(file_log,f"succesfull DB operation in id {document['id']}\n")
        else:
            make_log(file_log,f"failed DB operation in id {document['id']}\n")
    except Exception as e:
        make_log(file_log," Got Error "+str(e)+"\n")