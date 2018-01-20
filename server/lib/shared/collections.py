from pymongo import MongoClient
from pprint import pprint
from bson.objectid import ObjectId

class Collection:
    def __init__(self, db, name):
        self.collection = db[name]

    def __str__(self):
        string = ''
        cursor = self.collection.find()
        for doc in cursor:
            pprint(doc)
        return ''

    def add(self, obj_to_add):
        return self.collection.insert_one(obj_to_add)

    def query(self, query):
        return self.collection.find(query)

    def query_one(self, query):
        return self.collection.find_one(query)

    def wipe(self):
        self.collection.remove({})


class ProductCollection(Collection):
    def __init__(self, db):
        Collection.__init__(self, db, 'Products')

    def add_product(self, name, alias, connected_node_ids, planar_position,
                    height):
        product = {
            'Name': name,
            'Alias': alias,
            'ConnectedNodeIds': connected_node_ids,
            'PlanarPosition': planar_position,
            'Height': height
        }
        result = Collection.add(self, product)
        return result.inserted_id

    def add_products_batch(self, products):
        result = self.collection.insert_many(products)
        return result.inserted_ids


class NodeCollection(Collection):
    def __init__(self, db):
        Collection.__init__(self, db, 'Nodes')

    def add_node(self, planar_position, linked_node_ids):
        node = {
            'PlanarPosition': planar_position,
            'LinkedNodeIds': linked_node_ids,
        }
        result = Collection.add(self, node)
        return result.inserted_id

    def add_linked_node_ids(self, node_id, new_linked_node_ids):
        if type(node_id) == 'str':
            node_id = ObjectId(node_id)
        self.collection.update_one({
            '_id': node_id
        }, {
            '$set': {
                'LinkedNodeIds': new_linked_node_ids
            }
        })


class StoreCollection(Collection):
    def __init__(self, db):
        Collection.__init__(self, db, 'Stores')

    def add_store(self, name, all_node_ids, product_ids):
        store = {
            'Name': name,
            'AllNodeIds': all_node_ids,
            'ProductIds': product_ids
        }
        result = Collection.add(self, store)
        return result.inserted_id


class QRCodeCollection(Collection):
    def __init__(self, db):
        Collection.__init__(self, db, 'QRCodes')


    def add_code(self, store_id, store_name, transform):
        result = self.collection.add({
            'StoreId': store_id,
            'StoreName': store_name,
            'Transform': transform
        })
        return result.inserted_id
   
    def add_codes_batch(self, codes):
        result = self.collection.insert_many(codes)
        return result.inserted_ids

    def get_info(self, code):
        error = False
        try:
            code_id = ObjectId(code)
        except:
            error = True

        if error:
            raise ValueError("QR code \'%s\' is not valid" % code)
        
        data = self.collection.find_one({'_id': code_id})
        if data is None:
            raise ValueError("QR code \'%s\' cannot be found" % code)

        return data['StoreId'], data['Transform']
            