from autobounty.database import MONGO
from bson.objectid import ObjectId


class Domain:
    def __init__(self, parent_id=None, fqdn=None):
        self.parent_id = parent_id
        self.fqdn = fqdn

    # Todo:
    # - Find a way to remove the for loop (only one result expected)
    # - Can I replace ObjectId's with a string ID?
    @staticmethod
    def find_by_id(_id):
        search = MONGO.db.domains.find({'_id': {'$eq': ObjectId(_id)}})
        domains = []
        for domain in search:
            domains.append(domain)
        return domains


    @staticmethod
    def find_by_parent_id(parent_id):
        # Find one by parent ID (company identifier)
        search = MONGO.db.domains.find({'parent_id': {'$eq': parent_id}})
        domains = []
        for domain in search:
            domains.append(domain)
        return domains

    @staticmethod
    def find_all():
        # Find all domains
        search = MONGO.db.domains.find()
        domains = []
        for domain in search:
            domains.append(domain)
        # If company=True, scope to those results
        return domains

    def save(self):
        query = {'fqdn': self.fqdn}
        insert = {'parent_id': self.parent_id, 'fqdn': self.fqdn}
        MONGO.db.domains.update(query, insert, upsert=True)
        return True
