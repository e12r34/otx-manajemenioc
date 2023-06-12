#This program save the json get from otx_per_page_last_month.py to DB
import os, re, json, pymongo

from dotenv import load_dotenv
load_dotenv()

from custom_logging import make_log
from datetime import datetime

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["db_manajemen_ioc"]
collection = db["cl_pulse"]
collection_ioc=db["cl_ioc"]



file_log=open("log_save_db.log","a")
dir_path = os.getenv("PULSE_DIR")

file_list=os.listdir('./pulse')

#regex for hexadecimal file 24 char
pattern = re.compile(r'^[0-9a-f]{24}\.json$')

json_files = [f for f in file_list if f.endswith('.json') and pattern.match(f)]


for json_file in json_files:
    print(json_file)
    make_log(file_log,f"Processing file {json_file}")
    with open(dir_path+"/"+json_file, 'r') as f:
        try:
            json_data = json.load(f)
            indicators=json_data['indicators']
            del json_data['indicators']
            
            
            result = collection.find_one({'id': json_data['id']})
            Insert_Ioc=False
            if result:
            # If the modified field is different, update the document
                make_log(file_log,f"Updating Document to Collection IOC with id {json_data['id']}")
                if result['modified'] != json_data['modified']:
                    result_update=collection.update_one({'id': json_data['id']}, {'$set': json_data})
                    if result_update.modified_count>0:
                        print(f"Updated {result_update.modified_count} document(s).")
                        collection_ioc.delete_many({"otx_id":json_data['id']})
                        Insert_Ioc=True
                    else:
                        print(f"No Change made")
                        make_log(file_log,f"failed Updating Document to Collection IOC with id {json_data['id']}")
            else:
                # If the id does not exist, insert the document
                make_log(file_log,f"Inserting Document to Collection IOC with id {json_data['id']}")

                result_insert=collection.insert_one(json_data)
                if result_insert.inserted_id:
                    print('Document inserted with ID:', result_insert.inserted_id)
                    Insert_Ioc=True
                else:
                    print('Insert failed')
                    make_log(file_log,f"failed Insert Document to Collection IOC with id {json_data['id']}")
            if Insert_Ioc:
                for i in range(len(indicators)):
                    indicators[i]['otx_id']=json_data['id']
                collection_ioc.insert_many(indicators)            
            make_log(file_log,f"Success Insert Document to Collection IOC with id {json_data['id']}")

        except Exception as e:
            make_log(file_log,f"Got Error {str(e)}")
    os.remove(dir_path+"/"+json_file)