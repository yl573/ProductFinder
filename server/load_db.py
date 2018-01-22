from lib.product_search.main import ProductFinder
from lib.database_builder.main import DatabaseBuilder
from lib.qr_reader.main import QRReader
import sys
import os

from pymongo import MongoClient

if len(sys.argv) == 1:
    print("please specify which map to load")
    sys.exit()

db_url = 'mongodb://localhost:27017/',
db_name = 'ProductFinder'

client = MongoClient(db_url)
db = client[db_name]

builder = DatabaseBuilder(db)
builder.wipe_database()
builder.load_store_from_folder(os.path.dirname(__file__) + '/../Maps/' + sys.argv[1])
