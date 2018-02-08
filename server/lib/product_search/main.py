from ..shared.collections import (ProductCollection, NodeCollection,
                                  StoreCollection, ShelfCollection)
from .floor_map import FloorMap
from .matching import fuzzy_match
import numpy as np


def build_store_map(all_nodes):
    store_map = FloorMap()
    for node in all_nodes:
        store_map.add_node(node['_id'], node['PlanarPosition'],
                           node['LinkedNodeIds'])
    return store_map


def same_nodes(nodes1, nodes2):
    for n in nodes1:
        if n not in nodes2:
            return False
    return True


def find_nearest_entry_node(entry_nodes, current_position):
    min_dist = np.inf
    nearest_node_id = ''
    p1 = np.array(current_position)

    for node in entry_nodes:
        p2 = np.array(node['PlanarPosition'])
        dist = np.linalg.norm(p1 - p2)
        if dist < min_dist:
            min_dist = dist
            nearest_node_id = node['_id']

    return nearest_node_id


def find_path_to_product(product, connected_nodes, store_map, user_position):

    prod_intercept_pos, offset = find_aisle_intercept(
        product['PlanarPosition'], connected_nodes[0]['PlanarPosition'],
        connected_nodes[1]['PlanarPosition'])

    store_map.add_node(
        'Product Aisle Intercept',
        prod_intercept_pos,
        product['ConnectedNodeIds'],
        bidirectional=True)

    store_map.add_node(
        'Goal',
        product['PlanarPosition'], ['Product Aisle Intercept'],
        bidirectional=True)

    user_aisle_nodes = store_map.find_closest_edge(user_position)

    user_intercept_pos, _ = find_aisle_intercept(
        user_position, user_aisle_nodes[0].pos, user_aisle_nodes[1].pos)

    if same_nodes(
        [str(connected_nodes[0]['_id']),
         str(connected_nodes[1]['_id'])],
        [user_aisle_nodes[0].name, user_aisle_nodes[1].name]):
        # if we happen to be on the aisle of the product
        # just go the the product intercept
        connections = ['Product Aisle Intercept']
    else:
        connections = [n.name for n in user_aisle_nodes]

    store_map.add_node(
        'User Aisle Intercept',
        user_intercept_pos,
        connections,
        bidirectional=True)

    path = store_map.find_path('User Aisle Intercept', 'Goal')

    return path


def find_aisle_intercept(pos, node1_pos, node2_pos):
    p0 = np.array(pos)
    p1 = np.array(node1_pos)
    p2 = np.array(node2_pos)
    pdiff = p1 - p2
    unit = pdiff / np.linalg.norm(pdiff)
    magnitude = (p0 - p2).dot(unit)
    intercept = p2 + unit * magnitude
    offset = np.linalg.norm(p0 - intercept)

    return intercept, offset


def cursor_to_list(cursor):
    return [doc for doc in cursor]


class ProductFinder():
    def __init__(self, db):
        self.db = db
        self.products = ProductCollection(self.db)
        self.nodes = NodeCollection(self.db)
        self.stores = StoreCollection(self.db)
        self.shelves = ShelfCollection(self.db)

    def find_store(self, store_name):
        store = self.stores.query_one({'Name': store_name})
        if store is None:
            raise ValueError("The store \"%s\" is not found" % store_name)
        return store

    def find_matching_products(self, search_name, store_name):
        store = self.find_store(store_name)
        products_cursor = self.products.query({
            '_id': {
                '$in': store['ProductIds']
            }
        })
        results = fuzzy_match(search_name, cursor_to_list(products_cursor))

        return [r['Name'] for r in results]

    def find_product_in_store(self, product_name, store_name):
        store = self.find_store(store_name)
        product = self.products.query_one({
            '_id': {
                '$in': store['ProductIds']
            },
            'Name': product_name
        })

        if product is None:
            raise ValueError(
                "The product \"%s\" is not found in store \"%s\"" %
                (product_name, store_name))
        return product

    def get_product_shelf(self, product_name, store_name):
        product = self.find_product_in_store(product_name, store_name)
        shelf = self.shelves.query_one({'_id': product['ShelfId']})

        return (shelf['Name'], shelf['X1'], shelf['Y1'], shelf['X2'], shelf['Y2'])

    def search_path_to_product(self, product_name, store_name, user_position):
        product = self.find_product_in_store(product_name, store_name)

        # find all the data
        all_store_nodes = cursor_to_list(
            self.nodes.query({
                '_id': {
                    '$in': store['AllNodeIds']
                }
            }))

        connected_nodes = cursor_to_list(
            self.nodes.query({
                '_id': {
                    '$in': product['ConnectedNodeIds']
                }
            }))

        # compute path
        store_map = build_store_map(all_store_nodes)
        path = find_path_to_product(product, connected_nodes, store_map,
                                    user_position)
        return (path, product['Height'])