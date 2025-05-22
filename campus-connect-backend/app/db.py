from flask_pymongo import PyMongo

mongo = PyMongo()

def init_db(app):
    return mongo.db

def get_db():
    return mongo.db

def get_collection(collection_name):
    return mongo.db[collection_name]