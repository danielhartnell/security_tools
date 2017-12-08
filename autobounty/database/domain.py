from autobounty.database import MONGO


class Domain:
    def __init__(self, parent_id=None, fqdn=None):
        self.parent_id = parent_id
        self.fqdn = fqdn

    @staticmethod
    def find(fqdn):
        # Find one by company ID
        pass

    @staticmethod
    def find_all():
        # Find all domains
        search = MONGO.db.domains.find()
        domains = []
        for domain in search:
            domains.append(domain)
        # If company=True, scope to those results
        return domains

    @staticmethod
    def update():
        # Update x on n companies by y query
        pass

    def save(self):
        query = {'fqdn': self.fqdn}
        insert = {'parent_id': self.parent_id, 'fqdn': self.fqdn}
        MONGO.db.domains.update(query, insert, upsert=True)
        return True
