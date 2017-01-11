import pymongo

# todo: add logging
# todo: add these to configuration
client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
db = client['mud']
