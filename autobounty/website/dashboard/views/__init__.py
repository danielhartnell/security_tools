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
        company['matches'] = len(Domain.find(str(company['_id'])))
    return render_template('companies.html',
                           companies=companies,
                           title='Autobounty Dashboard')


@web.route('/<parent_id>')
def company_domains(parent_id):
    domains = Domain.find(parent_id)
    return render_template('domains.html',
                           domains=domains,
                           title='{} domains'.format(parent_id))


@web.route('/scan/<domain_id>')
def scan_results_web(domain_id):
    domain = database.find_domains_by_id(domain_id)
    fqdn = domain['fqdn']
    scan_active = 'null'
    if domain['active'] is bool:
        if domain['active'] is True:
            scan_active = 'True'
        else:
            scan_active = 'False'
    return render_template('scan.html',
                           domain=domain,
                           active=scan_active,
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
