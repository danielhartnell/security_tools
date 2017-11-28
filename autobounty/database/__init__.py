from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from autobounty.website.dashboard import web

# Todo:
# - Identify what's normal during __init__
# - I suspect I will handle handle the DB connection here
# - Ideally, I can make this somewhat modular to support changes
# - Each method should probably be moved into a class
# - All of these are specific to the dashboard / API / scanner
# - A class like database.autobounty.update_scan() might be good
# - Class should probably be in another file and instantiated here

mongo = PyMongo(web)

def find_all_companies():
    connection = mongo.db.domains
    companies = []
    for company in connection.find():
        companies.append({
            'company_id': company['company_id'],
            'company_name': company['company_name'],
            'fqdn': company['fqdn'],
            'last_scan': company['last_scan']
        })
    return companies

def find_domains_by_id(id):
    connection = mongo.db.domains
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
    connection = mongo.db.domains
    connection.update_one({
        'fqdn': fqdn
    },{
        '$set': {
            'scan_results': scan_results
        }
    }, upsert=True)

def find_domains_by_company_id(id):
    connection = mongo.db.domains
    domains = []
    for domain in connection.find({'company_id': id}):
        domains.append({
            'fqdn': domain['fqdn'],
            '_id': domain['_id']
        })
    return domains

def find(query):
    connection = mongo.db.domains
    domain = connection.find(query)
    return domain

def insert(data):
    query = {'fqdn': data['fqdn']}
    mongo.db.domains.update(query, data, upsert=True)
    return True

def update(data):
    query = {'fqdn': data['fqdn']}
    mongo.db.domains.update(query, data)
    return True

def delete(fqdn):
    mongo.db.domains.delete_one( {'fqdn': fqdn} )
    return True

def count(company_name):
    domains = []
    query = {'company_name': company_name}
    search = mongo.db.domains.find(query)
    for result in search:
        domains.append(result)
    return len(domains)
