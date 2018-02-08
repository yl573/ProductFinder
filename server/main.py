from lib.product_search.main import ProductFinder
from lib.database_builder.main import DatabaseBuilder
from lib.qr_reader.main import QRReader
import sys
from pymongo import MongoClient
 
import pprint
import json

from flask import Flask, request
app = Flask(__name__)


if len(sys.argv) == 1:
    print("please specify which map to load")
    sys.exit()

store_name = sys.argv[1]
port = 80
if len(sys.argv) == 3:
    port = sys.argv[2]




db_url='mongodb://localhost:27017/',
db_name='ProductFinder'


@app.route('/') # Testing purpose
def index():
    return 'Index Page'


@app.route('/findproduct', methods=['POST'])
def find_product():

    # print(json.dumps(request.form))
    name = request.form['name']

    client = MongoClient(db_url)
    db = client[db_name]

    finder = ProductFinder(db)
    results = finder.find_matching_products(name, store_name)

    return json.dumps({ "products": results })


@app.route('/findpath', methods=['POST'])
def find_path():

    product = request.form['product']
    position = request.form['position']

    position = tuple([float(x) for x in position[1:-1].split(',')])

    client = MongoClient(db_url)
    db = client[db_name]

    finder = ProductFinder(db)
    try:
        path, height = finder.search_path_to_product(product, store_name, position)
        return json.dumps({'path': [list(p) for p in path], 'height': height})
    except ValueError as e:
        return json.dumps({'error': str(e)})
    

@app.route('/findshelf', methods=['POST'])
def find_shelf():

    product = request.form['product']

    client = MongoClient(db_url)
    db = client[db_name]

    finder = ProductFinder(db)
    try:
        name, x1, y1, x2, y2 = finder.get_product_shelf(product, store_name)
        return json.dumps({
            'name': name,
            'left': [x1, y1],
            'right': [x2, y2]
        })
    except ValueError as e:
        return json.dumps({'error': str(e)})


app.run(host="0.0.0.0", port=port)