from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from autobounty.website.dashboard import web

MONGO = PyMongo(web)

# def find_all_companies():
#     connection = MONGO.db.domains
#     companies = []
#     for company in connection.find():
#         companies.append({
#             'company_id': company['company_id'],
#             'company_name': company['company_name'],
#             'fqdn': company['fqdn'],
#             'last_scan': company['last_scan']
#         })
#     return companies

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

def update_scan(fqdn, scan_results):
    connection = MONGO.db.domains
    connection.update_one({
        'fqdn': fqdn
    },{
        '$set': {
            'scan_results': scan_results
        }
    }, upsert=True)

def find_domains_by_company_id(id):
    connection = MONGO.db.domains
    domains = []
    for domain in connection.find({'company_id': id}):
        domains.append({
            'fqdn': domain['fqdn'],
            '_id': domain['_id']
        })
    return domains

def find(query):
    connection = MONGO.db.domains
    domain = connection.find(query)
    return domain

def insert(data):
    query = {'fqdn': data['fqdn']}
    MONGO.db.domains.update(query, data, upsert=True)
    return True

def update(data):
    query = {'fqdn': data['fqdn']}
    MONGO.db.domains.update(query, data)
    return True

def delete(fqdn):
    MONGO.db.domains.delete_one( {'fqdn': fqdn} )
    return True

def count(company_name):
    domains = []
    query = {'company_name': company_name}
    search = MONGO.db.domains.find(query)
    for result in search:
        domains.append(result)
    return len(domains)
