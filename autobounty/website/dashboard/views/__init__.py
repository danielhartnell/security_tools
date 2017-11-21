from autobounty.website.dashboard import web
from autobounty.website.dashboard import mongo
from flask import render_template


@web.route('/')
@web.route('/dashboard')
def index():
    all_results = mongo.db.domains
    domains = []
    for e in all_results.find():
        domains.append({'org': e['org'], 'fqdn': e['fqdn']})

    return render_template('index.html',
                           domains=domains,
                           title='autoscan dashboard')
