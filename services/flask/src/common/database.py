import os

import pymongo


class Database(object):
    # URI = "mongodb://127.0.0.1:27017"
    URI = 'mongodb://{}:27017'.format(os.environ.get('MONGODB_HOSTNAME', '127.0.0.1'))
    # URI = 'mongodb://' + os.environ.get(['MONGODB_HOSTNAME'], "127.0.0.1") + ':27017'
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['parking']
        Database.DATABASE['spots'].create_index([("loc", pymongo.GEO2D)])

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_range(sw, ne):
        return Database.DATABASE['spots'].find({'loc': {'$geoWithin': {'$box': [sw, ne]}}}).sort('upload_time', -1)

    @staticmethod
    def find_one(collection, query):
        result = Database.DATABASE[collection].find_one(query)
        return result

    @staticmethod
    def update(collection, query, data):
        Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def remove(collection, query):
        return Database.DATABASE[collection].remove(query)
