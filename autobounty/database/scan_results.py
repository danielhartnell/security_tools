from autobounty.database import MONGO


class Company:
    def __init__(self, id_=None, scan_results={}):
        self.id_ = id_,
        self.scan_results = scan_results

    @staticmethod
    def find(id_):
        # Find one by company ID
        pass

    @staticmethod
    def find_all():
        # Find all companies
        search = MONGO.db.scan_results.find()
        scans = []
        for scan in search:
            scans.append(scan)
        return scans

    @staticmethod
    def update():
        # Update x on n companies by y query
        pass

    def save(self):
        pass
