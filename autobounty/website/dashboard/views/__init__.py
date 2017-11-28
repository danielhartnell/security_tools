from flask import render_template

from autobounty import database
from autobounty.scanner import tasks
from autobounty.website.dashboard import web
import datetime


# Todo: Use API backend when relevant
# Find helper functions for repeating patterns
# Sanitize user input
# Could be fun to define a data type that will parse all inputs

@web.route('/')
@web.route('/dashboard')
def index():
    companies = []
    unique_companies = []
    search = database.find_all_companies()
    for result in search:
        if result['last_scan'] is not int:
            result['last_scan'] = 1
        date = datetime.datetime.fromtimestamp(result['last_scan']).strftime('%Y-%m-%d')
        companies.append({
            'company_name': result['company_name'],
            'company_id': result['company_id'],
            'last_scan': date,
            'matches': database.count(result['company_name'])
        })
    unique_companies = list({v['company_name']: v for v in companies}.values())
    # Stop adding match total to every company object (slow)
    return render_template('companies.html',
                           companies=unique_companies,
                           title='Autobounty Dashboard')

@web.route('/scan/headers')
def scan_headers():
    tasks.header_scan_subdomains.delay()
    return 'Initiated Celery background task to scan all domains.'

@web.route('/scan')
def scan():
    tasks.enumerate_subdomains.delay()
    return 'Scanning subdomains'

# Create a new route to view a specific org
# Query DB for all domains under that org
# Only show orgs with links on the dashboard
@web.route('/<id>')
@web.route('/dashboard/<id>')
def dashboard(id):
    domains = database.find_domains_by_company_id(id)
    return render_template('domains.html',
                           domains=domains,
                           title='Dashboard for a specific org')

@web.route('/scan/<id>')
@web.route('/dashboard/scan/<id>')
def scan_results_web(id):
    domain = database.find_domains_by_id(id)
    fqdn = domain['fqdn']
    scan_active = 'null'
    if domain['active'] is bool:
        if domain['active'] is True:
            scan_active = 'True'
        else:
            scan_active = 'False'
    #if domain['']
    return render_template('scan.html',
                           domain=domain,
                           active=scan_active,
                           title='Scan: {}'.format(fqdn))

# Domain overview page
    # Show domain response
        # Response code or connection status (timeout)
        # Response headers
