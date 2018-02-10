from lib.product_search.main import ProductFinder
from lib.database_builder.main import DatabaseBuilder 
from lib.database_builder.shelf_only_temp import ShelfOnlyDatabaseBuilder
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

map_path = os.path.dirname(os.path.realpath(__file__)) + '/../Maps/' + sys.argv[1]

# builder = DatabaseBuilder(db)
builder = ShelfOnlyDatabaseBuilder(db)
builder.wipe_database()
builder.load_shelves_and_products(map_path+'/shelves.json', map_path+'/products.csv', sys.argv[1])
