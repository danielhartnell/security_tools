from flask import Flask

web = Flask(__name__)
web.config.from_object('autobounty.conf.default_settings')

from autobounty.website.dashboard import views
from autobounty.website import api
from autobounty.scanner import tasks

# Todo: How do I deal with unused imports?
# Is there a different way to accomplish this?