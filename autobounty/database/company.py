from autobounty.database import MONGO


class Company:
    """
    Company object in MongoDB:
    {
      "_id"   : ObjectId,
      "name"  : "New Relic",
      "active": "True"
    }
    """
    def __init__(self, name=None, active=True):
        self.name = name
        self.active = active

    def save(self):
        query = {'name': self.name}
        insert = {'name': self.name, 'active': self.active}
        MONGO.db.companies.update(query, insert, upsert=True)
        return True

    @staticmethod
    def find():
        # Find one by company ID
        pass

    @staticmethod
    def find_all(unique=False):
        # Find all companies
        search = MONGO.db.companies.find()
        companies = []
        for company in search:
            companies.append(company)
        if unique is True:
            companies = list({v['name']: v for v in companies}.values())
        return companies
