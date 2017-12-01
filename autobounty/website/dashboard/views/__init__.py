import datetime

from flask import render_template
from autobounty import database
from autobounty.scanner import tasks
from autobounty.website.dashboard import web
from autobounty.database.company import Company

@web.route('/')
@web.route('/dashboard')
def index():
    companies = Company.find_all(unique=True)
    for company in companies:
        company['matches'] = database.count(company['company_name'])
    return render_template('companies.html',
                           companies=companies,
                           title='Autobounty Dashboard')


@web.route('/<company_id>')
@web.route('/dashboard/<company_id>')
def dashboard(company_id):
    domains = database.find_domains_by_company_id(company_id)
    company_name = domains[0]['company_name']
    return render_template('domains.html',
                           domains=domains,
                           title='{} dashboard'.format(company_name))


@web.route('/scan/<domain_id>')
@web.route('/dashboard/scan/<domain_id>')
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


@web.route('/scan')
def scan():
    tasks.enumerate_subdomains.delay()
    return 'Scanning domains'


@web.route('/scan/headers')
def scan_headers():
    tasks.header_scan_subdomains.delay()
    return 'Initiated Celery background task to scan all domains.'
