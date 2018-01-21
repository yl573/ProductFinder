from lib.product_search.main import ProductFinder
from lib.database_builder.main import DatabaseBuilder
from lib.qr_reader.main import QRReader

from pymongo import MongoClient

db_url='mongodb://localhost:27017/',
db_name='ProductFinder'

client = MongoClient(db_url)
db = client[db_name]

builder = DatabaseBuilder(db)
builder.wipe_database()
builder.load_store_from_folder('../EnginDept')