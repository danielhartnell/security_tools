from flask import request, jsonify

from autobounty import database
from autobounty.website.dashboard import web as api

# Todo: Put similar routes together
# Review other APIs to get a sense for structure
# Figure out a route naming scheme that's consistent
# Once the DB helpers are configured, adjust input params here

# Todo: Write tests to validate all routes

@api.route('/api/domains/create', methods=['POST'])
def create():
    """
    :required params: company_id, company_name, fqdn
    :return: database insert result (boolean)
    :todo: sanitize input
    """
    data = {
        'company_id': request.json['company_id'],
        'company_name': request.json['company_name'],
        'fqdn': request.json['fqdn'],
        'last_scan': None,
        'active': True,
        'scan_results': {}
    }
    database.insert(data)

    # Todo: validate insert success and wrap in try except
    return jsonify({'status': 'success'})

# Todo: Find repeating patterns and write helper methods
@api.route('/api/companies', methods=['GET'])
def show_companies():
    companies = []
    search = database.find_all_companies()
    for result in search:
        companies.append(result['company_name'])

    return jsonify({'status': 'success',
                    'response': companies})

@api.route('/api/domains', methods=['GET'])
def show_domains():
    domains = []
    search = database.find_all_companies()
    for result in search:
        domains.append(result['fqdn'])

    return jsonify({'status': 'success',
                    'response': domains})

@api.route('/api/domains/scan/update', methods=['POST'])
def update_scan():
    database.update_scan(request.json['fqdn'], request.json['scan_results'])
    return 'Updated record...'

@api.route('/api/domains/scan', methods=['GET'])
def scan_results():
    domain = database.find({'fqdn': 'synthetics.newrelic.com'})
    response = []
    for e in domain:
        response.append(e)
    return str(response)

@api.route('/api/domains/delete', methods=['DELETE'])
def delete():
    fqdn = request.json['fqdn']
    database.delete(fqdn)
    return 'Deleted record...'
