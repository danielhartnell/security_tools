from flask import render_template, request
from autobounty.scanner import tasks
from autobounty.website.dashboard import web
from autobounty.database.company import Company
from autobounty.database.domain import Domain
from wtforms import Form, BooleanField, StringField, validators


class CreateCompanyForm(Form):
    name = StringField('Name (example: "New Relic")', [validators.Length(min=2, max=25)])
    active = BooleanField('Enable automated scanning (does not function today)', [validators.DataRequired()])


class CreateDomainForm(Form):
    fqdn = StringField('FQDN (example: "newrelic.com")', [validators.Length(min=2, max=100)])
    parent_id = StringField('Parent ID (example: "5a224007abd70f12251dec69")', [validators.Length(min=2, max=64)])


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


@web.route('/company/create', methods=['GET', 'POST'])
def create_company():
    form = CreateCompanyForm(request.form)
    if request.method == 'POST' and form.validate():
        company = Company(
            name=form.name.data,
            active=form.active.data
        )
        company.save()
        return 'New company has been added'
    return render_template('new_company.html',
                           title='Create new company',
                           form=form)


@web.route('/domain/create', methods=['GET', 'POST'])
def create_domain():
    form = CreateDomainForm(request.form)
    if request.method == 'POST' and form.validate():
        domain = Domain(
            fqdn=form.fqdn.data,
            parent_id=form.parent_id.data
        )
        domain.save()
        return 'New domain has been added'
    return render_template('new_domain.html',
                           title='Create new domain',
                           form=form)


@web.route('/scan')
def scan():
    tasks.enumerate_subdomains.delay()
    return 'Scanning domains'


@web.route('/scan/headers')
def scan_headers():
    tasks.header_scan_subdomains.delay()
    return 'Initiated Celery background task to scan all domains.'
