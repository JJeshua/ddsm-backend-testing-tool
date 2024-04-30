import pymongo


from tests.base_test import BaseTestClass


NUM_OF_USERS = 100


def clear_all_collections(db):
    for collection_name in db.list_collection_names():
        db[collection_name].delete_many({})
        print(f"Cleared collection: {collection_name}")


print('Populating DB.')

mongo_client = pymongo.MongoClient("mongodb://localhost:27017")
db_name = "DuckPond"

# Connect to the database
db = mongo_client[db_name]

posts = []

users = [BaseTestClass() for _ in range(NUM_OF_USERS)]


# Close the MongoDB connection
mongo_client.close()

print("Successfully populated MongoDB")
