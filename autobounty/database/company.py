from autobounty.database import MONGO

class Company:
    def __init__(self, company_id=None, name=None, fqdn=None):
        self.company_id = company_id,
        self.name = name,
        self.fqdn = fqdn

    @staticmethod
    def find(company_id):
        # Find one by company ID
        pass

    @staticmethod
    def find_all(unique=False):
        # Find all companies
        search = MONGO.db.domains.find()
        companies = []
        for company in search:
            companies.append(company)
        if unique is True:
            companies = list({v['company_name']: v for v in companies}.values())
        return companies

    def update(self):
        # Update x on n companies by y query
        pass

    def save(self):
        pass

