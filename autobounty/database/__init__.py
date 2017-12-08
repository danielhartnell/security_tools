from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from autobounty.website.dashboard import web

MONGO = PyMongo(web)


def find_domains_by_id(id):
    connection = MONGO.db.domains
    domain = []
    for e in connection.find({'_id': ObjectId(id)}):
        domain.append({
            'company_id': e['company_id'],
            'company_name': e['company_name'],
            'fqdn': e['fqdn'],
            'last_scan': e['last_scan'],
            '_id': e['_id'],
            'active': e['active'],
            'scan_results': e['scan_results']
        })
    return domain[0]
