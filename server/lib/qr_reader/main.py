from ..shared.collections import StoreCollection, QRCodeCollection
from bson.objectid import ObjectId

class QRReader():

    def __init__(self, db):
        self.db = db
        self.stores = StoreCollection(self.db)
        self.qr_codes = QRCodeCollection(self.db)

    def get_info(self, code):
        store_id, transform = self.qr_codes.get_info(code)
        store = self.stores.query_one({'_id': store_id})

        return store['Name'], transform

    def find_codes_for_store(self, store_name): # used when deploying the QR codes
        results = self.qr_codes.query({'StoreName': store_name})
        return [str(x['_id']) for x in results]