import datetime

from flask import render_template, request, jsonify
from autobounty import database
from autobounty.scanner import tasks
from autobounty.website.dashboard import web
from autobounty.database.company import Company
from autobounty.database.domain import Domain


@web.route('/')
def index():
    companies = Company.find_all(unique=True)
    for company in companies:
        # ObjectId, _id, must be converted to type string
        # Open to recommendations on improving this
        parent_id = str(company['_id'])
        company['matches'] = len(Domain.find_by_parent_id(parent_id))
    return render_template('companies.html',
                           companies=companies,
                           title='Autobounty Dashboard')


@web.route('/<parent_id>')
def company_domains(parent_id):
    domains = Domain.find_by_parent_id(parent_id)
    return render_template('domains.html',
                           domains=domains,
                           title='{} domains'.format(parent_id))


@web.route('/scan/<_id>')
def scan_results_web(_id):
    domain = Domain.find_by_id(_id)
    if len(domain) > 1:
        return 'Error: too many results from DB query'
    fqdn = domain[0]['fqdn']
    return render_template('scan.html',
                           domain=domain[0],
                           title='Scan: {}'.format(fqdn))


@web.route('/company/create', methods=['POST'])
def create_company():
    company = Company(
        name=request.json['name'],
        active=request.json['active']
    )
    company.save()
    return jsonify({'create_company': 'success'})


@web.route('/domain/create', methods=['POST'])
def create_domain():
    domain = Domain(
        parent_id=request.json['parent_id'],
        fqdn=request.json['fqdn']
    )
    domain.save()
    return jsonify({'create_domain': 'success'})


@web.route('/scan')
def scan():
    tasks.enumerate_subdomains.delay()
    return 'Scanning domains'


@web.route('/scan/headers')
def scan_headers():
    tasks.header_scan_subdomains.delay()
    return 'Initiated Celery background task to scan all domains.'
