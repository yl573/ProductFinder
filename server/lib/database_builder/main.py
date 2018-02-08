from ..shared.collections import (ProductCollection, NodeCollection, 
StoreCollection, QRCodeCollection, ShelfCollection)
from os import path
import json
import pandas as pd
import numpy as np


def get_file_paths(folder_path):
    abs_folder_path = path.abspath(folder_path)
    products_path = path.join(abs_folder_path, 'products.csv')
    nodes_path = path.join(abs_folder_path, 'nodes.csv')
    store_path = path.join(abs_folder_path, 'store.json')

    if not path.exists(products_path):
        raise ValueError(
            "\'products.csv\' not found under path %s" % abs_folder_path)
    elif not path.exists(nodes_path):
        raise ValueError(
            "\'nodes.csv\' not found under path %s" % abs_folder_path)
    elif not path.exists(store_path):
        raise ValueError(
            "\'store.json\' not found under path %s" % abs_folder_path)

    return (products_path, nodes_path, store_path)


def string_to_array(string):
    return [float(x) for x in string.split()]


def save_nodes(nodes_df, node_collection):
    nodes_df = nodes_df.set_index("Index")
    index_to_id = {}
    for i, node in nodes_df.iterrows():
        node_dict = node.to_dict()
        position = tuple(string_to_array(node_dict['Coordinate']))
        node_id = node_collection.add_node(position, [])
        index_to_id[i] = node_id

    for i in index_to_id.keys():
        node_id = index_to_id[i]
        linked_nodes = string_to_array(
            nodes_df.loc[i, 'Connected Nodes'])
        linked_node_ids = [index_to_id[n] for n in linked_nodes]
        node_collection.add_linked_node_ids(node_id, linked_node_ids)

    return index_to_id


# def calc_planar_position(parent_coord_str, rel_coord_str):
#     p1 = string_to_array(parent_coord_str)
#     p2 = string_to_array(rel_coord_str)
#     return (p1[0]+p2[0], p1[1]+p2[1])


def save_products(product_df, index_to_id, product_collection):
    products = []
    for i, product in product_df.iterrows():
        aisle_nodes = string_to_array(product['Aisle Nodes'])
        products.append({
            'Name':
            product['Name'],
            'Alias':
            product['Alias'],
            'ConnectedNodeIds': [index_to_id[n] for n in aisle_nodes],
            'PlanarPosition':
            [product['X Coordinate'], product['Y Coordinate']],
            'Height':
            product['Height']
        })
    product_ids = product_collection.add_products_batch(products)
    return product_ids


def save_qr_codes(store_id, store, qr_collection):
    qr_codes = [
        {
            'StoreId': store_id,
            'StoreName': store['Name'],
            'Transform': code['Transform']
        }  
        for code in store['QR Codes']
    ]
    qr_collection.add_codes_batch(qr_codes)


def save_store(store, store_collection, product_ids, index_to_id):
    return store_collection.add_store(store['Name'], list(index_to_id.values()), product_ids)

class ShelfOnlyDatabaseBuilder():
    def __init__(self, db):
        self.db = db
        self.products = ProductCollection(self.db)
        self.stores = StoreCollection(self.db)
        self.shelves = ShelfCollection(self.db)

    def load_shelves_and_products(self, shelf_csv, products_csv, store_name):
        name_id_map = self.load_shelves(shelf_csv)
        product_ids = self.load_products(products_csv, name_id_map)
        self.stores.add_store(store_name, None, product_ids)
        print('Database loaded')

    def load_shelves(self, csv_path):
        df = pd.read_csv(csv_path)
        name_id_map = {}
        for _, s in df.iterrows():
            shelf_id = self.shelves.add_shelf(s['Name'], s['X1'], s['Y1'], s['X2'], s['Y2'])
            name_id_map[s['Name']] = shelf_id
        return name_id_map

    def load_products(self, csv_path, name_id_map):
        df = pd.read_csv(csv_path)
        product_ids = []
        for _, p in df.iterrows():
            product_ids.append(self.products.add_product(p['Name'], name_id_map[p['Shelf']]))
        return product_ids

    def wipe_database(self):
        self.products.wipe()
        self.stores.wipe()
        self.shelves.wipe()
        print('Database wiped')


        

class DatabaseBuilder():
    def __init__(self, db):
        self.db = db
        self.products = ProductCollection(self.db)
        self.nodes = NodeCollection(self.db)
        self.stores = StoreCollection(self.db)
        self.qr_codes = QRCodeCollection(self.db)

    def load_store_from_folder(self, folder_path):

        products_path, nodes_path, store_path = get_file_paths(folder_path)

        products = pd.read_csv(products_path)
        nodes = pd.read_csv(nodes_path)
        with open(store_path, 'r') as json_file:
            store = json.load(json_file)

        index_to_id = save_nodes(nodes, self.nodes)
        product_ids = save_products(products, index_to_id, self.products)
        store_id = save_store(store, self.stores, product_ids, index_to_id)
        save_qr_codes(store_id, store, self.qr_codes)

        print('Database loaded')

    def wipe_database(self):

        self.products.wipe()
        self.nodes.wipe()
        self.stores.wipe()
        self.qr_codes.wipe()

        print('Database wiped')
