from flask import Flask
from flask_pymongo import PyMongo

web = Flask(__name__)

web.config.update(MONGO_DBNAME='secmon')
web.config.update(MONGO_URI='mongodb://localhost:27017/secmon')

mongo = PyMongo(web)

from autobounty.website.dashboard import views
from autobounty.website import api
