import pymongo


def clear_all_collections(db):
    for collection_name in db.list_collection_names():
        db[collection_name].delete_many({})
        print(f"Cleared collection: {collection_name}")


print("Clearing MongoDB.")

mongo_client = pymongo.MongoClient("mongodb://localhost:27017")
db_name = "DuckPond"

# Connect to the database
db = mongo_client[db_name]

# Clear all collections
clear_all_collections(db)

# Close the MongoDB connection
mongo_client.close()

print("Successfully cleared MongoDB")
