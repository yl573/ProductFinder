from lib.product_search.main import ProductFinder
from lib.database_builder.main import DatabaseBuilder
from lib.qr_reader.main import QRReader

from pymongo import MongoClient
 
import pprint
import json

from flask import Flask, request
app = Flask(__name__)


db_url='mongodb://localhost:27017/',
db_name='ProductFinder'


@app.route('/') # Testing purpose
def index():
    return 'Index Page'


@app.route('/findproduct', methods=['POST'])
def find_product():

    name = request.form['name']

    client = MongoClient(db_url)
    db = client[db_name]

    finder = ProductFinder(db)
    results = finder.find_matching_products(name, 'Coop')
    responseObject = {
        "products": results
    }

    return json.dumps(responseObject)


@app.route('/findpath', methods=['POST'])
def find_path():

    product = request.form['product']
    position = request.form['position']

    position = tuple([float(x) for x in position[1:-1].split(',')])

    client = MongoClient(db_url)
    db = client[db_name]

    finder = ProductFinder(db)
    path, height = finder.search_path_to_product(product, 'Coop', position)
    print(pprint.pformat(path))
    return json.dumps({'path': [list(p) for p in path], 'height': height})
