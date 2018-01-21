from lib.product_search.main import ProductFinder
from lib.database_builder.main import DatabaseBuilder
from lib.qr_reader.main import QRReader

from pymongo import MongoClient
import pprint

db_url='mongodb://localhost:27017/',
db_name='ProductFinder'

client = MongoClient(db_url)
db = client[db_name]

# builder = DatabaseBuilder(db)
# builder.wipe_database()
# builder.load_store_from_folder('./EnginDept')

# reader = QRReader(db)
# qr_codes = reader.find_codes_for_store('Coop')
# print('QR codes: ', qr_codes)

# store, transform = reader.get_info(qr_codes[0])
# print('store: ', store)
# print('QR code transform: ', transform)

finder = ProductFinder(db)
results = finder.find_matching_products('c', 'Department')
print('results: ', pprint.pformat(results))

if len(results) > 0:
    path, height = finder.search_path_to_product(results[0], 'Department', (0,0))
    print('path: ', pprint.pformat(path))
    print('height: ', height)