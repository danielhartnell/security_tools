from celery import Celery
from celery.schedules import crontab
from autobounty.website.dashboard import web

# Task module imports
from sublist3r import sublist3r
from tld import get_tld
import time

def make_celery(i):
    celery = Celery(web.import_name)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with web.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

app = make_celery(web)
app.config_from_object('autobounty.conf.default_settings')

# General tasks
@app.task(name='enumerate_subdomains')
def enumerate_subdomains():
    from autobounty import database
    domains = []
    apex_domains = []
    unique_apex_domains = []
    search = database.find_all_companies()
    for result in search:
        domains.append({
            'company_name': result['company_name'],
            'company_id': result['company_id'],
            'fqdn': result['fqdn'],
        })
    for domain in domains:
        apex = get_tld('http://' + str(domain['fqdn']))
        apex_domains.append({'company_name': domain['company_name'], 'company_id': domain['company_id'], 'fqdn': apex})
    unique_apex_domains = list({v['fqdn']: v for v in apex_domains}.values())
    for domain in unique_apex_domains:
        engines = 'virustotal,threatcrowd,ssl,dnsdumpster,netcraft'
        scan_output = sublist3r.main(domain['fqdn'], 30, '',
                                     False, False, False, False, engines)
        for result in scan_output:
            print('Adding domain {} from {}'.format(domain['company_name'], result))
            data = {
                'company_id': domain['company_id'],
                'company_name': domain['company_name'],
                'fqdn': result,
                'last_scan': time.time(),
                'active': True,
                'scan_results': {}
            }
            database.insert(data)
    return True

@app.task(name='header_scan_subdomains')
def header_scan_subdomains():
    from autobounty import database
    import requests
    domains = []
    search = database.find_all_companies()
    for result in search:
        domains.append(result['fqdn'])
    for domain in domains:
        try:
            req = requests.head('http://' + domain)
            print('Captured response code: ' + str(req.status_code))
            response_code = req.status_code
            headers = req.headers
            scan_results = {'response_code': str(response_code), 'response_headers': headers}
            database.update_scan(domain, scan_results)
        except requests.ConnectionError:
            print('Failed to connect to: ' + domain)
            scan_results = {'response_code': 'ConnectionError', 'response_headers': {'ConnectionError': 'ConnectionError'}}
            database.update_scan(domain, scan_results)
        time.sleep(1)
    return True

# Scheduled tasks
@app.task(run_every=(crontab(minute='*/1')), name='some_task', ignore_result=True)
def some_task():
    print('I am a schedule task')
