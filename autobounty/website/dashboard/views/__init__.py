import datetime

from flask import render_template
from autobounty import database
from autobounty.scanner import tasks
from autobounty.website.dashboard import web


@web.route('/')
@web.route('/dashboard')
def index():
    companies = []
    search = database.find_all_companies()
    for result in search:
        if result['last_scan'] is not int:
            result['last_scan'] = 1
        date = datetime.datetime.fromtimestamp(result['last_scan']).strftime('%Y-%m-%d')
        companies.append({
            'company_name': result['company_name'],
            'company_id': result['company_id'],
            'last_scan': date
        })
    unique_companies = list({v['company_name']: v for v in companies}.values())
    for c in unique_companies:
        c['matches'] = database.count(c['company_name'])

    # Look at an ordered dictionary
    # cache_property decorator
    return render_template('companies.html',
                           companies=unique_companies,
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
