from flask import Flask

web = Flask(__name__)
web.config.from_object('autobounty.conf.default_settings')

from autobounty.website.dashboard import views
from autobounty.scanner import tasks
