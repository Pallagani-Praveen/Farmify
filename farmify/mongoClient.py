import pymongo

class MongoClient:
    def __init__(self):
        self.username = 'praveen'
        self.password = 'praveen'
        self.db = 'Farmify'
        self.newsKey = 'cd9774bdb78d482f8161739f5166e804'
    
    def getConnection(self,):
        try:
            return pymongo.MongoClient("mongodb+srv://"+self.username+":"+self.password+"@framifycluster.hromh.mongodb.net/"+self.db+"?retryWrites=true&w=majority")
        except ConnectionError:
            return None
            

    def getNewsKey(self):
        return self.newsKey
