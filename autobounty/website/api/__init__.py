from autobounty.website.dashboard import web as api
from autobounty.website.dashboard import mongo
from flask import request, jsonify


@api.route('/api/domains')
def list():
    all_results = mongo.db.domains
    domains = []
    for e in all_results.find():
        domains.append({'org': e['org'], 'fqdn': e['fqdn']})

    return jsonify(domains)

@api.route('/api/domains/create', methods=['POST'])
def create():
    organization = request.json['organization']
    fqdn = request.json['fqdn']
    return jsonify({'result': {
        'organization': organization,
        'fqdn': fqdn
    }})
