import pymongo


def connectToDataBase():
    myClient = pymongo.MongoClient('mongodb://localhost:27017/')
    myDataBase = myClient['dantri']
    myCollection = myDataBase['news']
    return myCollection


def insertToDataBase(key, value, dataBase):
    dataBase.update_one(key, value, upsert=True)
