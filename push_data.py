import os
import sys
import json
from dotenv import load_dotenv
import pymongo.mongo_client
import pymongo.monitoring

load_dotenv()

MONGO_DB_URI = os.getenv('MONGO_URI')

import certifi ## 
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_json_convertor(self,filepath):
        try:
            data = pd.read_csv(filepath)
            data.reset_index(drop=True,inplace=True) ##for to remove default index from database

            records = list(json.loads(data.T.to_json()).values()) ## transpose and then convert json to get proper list of json format

            return records
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def insert_data_mongo(self, records, database_name, collection_name):
        try:
            # Create MongoDB client
            mongo_client = pymongo.MongoClient(MONGO_DB_URI, tls=True, tlsCAFile=ca)

            # Access database and collection
            db = mongo_client[database_name]
            collection = db[collection_name]

            # Insert records
            collection.insert_many(records)

            return len(records)

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
if __name__ == "__main__":

    FILE_PATH = "Network_Data\phisingData.csv"
    DATABASE = "ARSATHAI"
    collection = "NetworkData"
    networkobj = NetworkDataExtract()
    records = networkobj.csv_json_convertor(FILE_PATH)


    no_of_records = networkobj.insert_data_mongo(records,DATABASE,collection)

    print(no_of_records)
