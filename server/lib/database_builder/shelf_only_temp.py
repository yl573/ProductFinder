# this is disposable code

from ..shared.collections import (ProductCollection, NodeCollection,
                                  StoreCollection, QRCodeCollection,
                                  ShelfCollection)
from os import path
import json
import pandas as pd
import numpy as np


class ShelfOnlyDatabaseBuilder():
    def __init__(self, db):
        self.db = db
        self.products = ProductCollection(self.db)
        self.stores = StoreCollection(self.db)
        self.shelves = ShelfCollection(self.db)

    def load_shelves_and_products(self, shelf_json, products_csv, store_name):
        name_id_map = self.load_shelves(shelf_json)
        product_ids = self.load_products(products_csv, name_id_map)
        self.stores.add_store(store_name, None, product_ids)
        print('Database loaded')

    def load_shelves(self, json_path):
        with open(json_path, 'r') as f:
            data = json.load(f)
        name_id_map = {}
        target = list(filter(lambda x: x['name'] == 'Target', data))[0]
        for d in data:
            shelf_id = self.shelves.add_shelf(
                d['name'], 
                d['startPos']['x'] - target['startPos']['x'], 
                d['startPos']['y'] - target['startPos']['y'],
                d['endPos']['x'] - target['endPos']['x'], 
                d['endPos']['y'] - target['endPos']['y'])
                # d['actualStartPos']['x'] - target['actualStartPos']['x'], 
                # d['actualStartPos']['y'] - target['actualStartPos']['y'],
                # d['actualEndPos']['x'] - target['actualEndPos']['x'], 
                # d['actualEndPos']['y'] - target['actualEndPos']['y'])
            name_id_map[d['name']] = shelf_id
        return name_id_map

    def load_products(self, csv_path, name_id_map):
        df = pd.read_csv(csv_path)
        product_ids = []
        for _, p in df.iterrows():
            product_ids.append(
                self.products.add_product(p['Name'], name_id_map[p['Shelf']]))
        return product_ids

    def wipe_database(self):
        self.products.wipe()
        self.stores.wipe()
        self.shelves.wipe()
        print('Database wiped')