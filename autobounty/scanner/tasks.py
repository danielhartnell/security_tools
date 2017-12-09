import time
from tld import get_tld
from sublist3r import sublist3r
from celery import Celery
from celery.schedules import crontab
from autobounty.website.dashboard import web
from autobounty.database.domain import Domain


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
    domains = Domain.find_all()
    apex_domains = []
    for domain in domains:
        apex = get_tld('http://' + str(domain['fqdn']))
        apex_domains.append({'parent_id': domain['parent_id'], 'fqdn': apex})
    unique_apex_domains = list({v['fqdn']: v for v in apex_domains}.values())
    for domain in unique_apex_domains:
        engines = 'virustotal,threatcrowd,ssl,dnsdumpster,netcraft'
        scan_output = sublist3r.main(domain['fqdn'], 30, '',
                                     False, False, False, False, engines)
        for result in scan_output:
            print('Adding domain {} from {}'.format(result, domain['parent_id']))
            new_domain = Domain(
                parent_id=domain['parent_id'],
                fqdn=result
            )
            new_domain.save()
    return True

# @app.task(name='header_scan_subdomains')
# def header_scan_subdomains():
#     from autobounty import database
#     import requests
#     domains = []
#     search = database.find_all_companies()
#     for result in search:
#         domains.append(result['fqdn'])
#     for domain in domains:
#         try:
#             req = requests.head('http://' + domain)
#             print('Captured response code: ' + str(req.status_code))
#             response_code = req.status_code
#             headers = req.headers
#             scan_results = {'response_code': str(response_code), 'response_headers': headers}
#             database.update_scan(domain, scan_results)
#         except requests.ConnectionError:
#             print('Failed to connect to: ' + domain)
#             scan_results = {'response_code': 'ConnectionError', 'response_headers': {'ConnectionError': 'ConnectionError'}}
#             database.update_scan(domain, scan_results)
#         time.sleep(1)
#     return True

# Scheduled tasks
@app.task(run_every=(crontab(minute='*/1')), name='some_task', ignore_result=True)
def some_task():
    print('I am a schedule task')
