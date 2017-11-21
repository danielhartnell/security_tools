from flask_pymongo import PyMongo
from autobounty.website.dashboard import web

def conn(self):
    return PyMongo(web)
