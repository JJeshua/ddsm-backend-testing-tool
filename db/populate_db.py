import pymongo
from random import random

from tests.base_user import BaseUser


NUM_OF_USERS = 5
NUM_OF_POSTS_PER_USER = 15
USER_PROBABILITY_TO_LIKE = 0.345
USER_PROBABILITY_TO_COMMENT = 0.123


print('Populating DB.')

mongo_client = pymongo.MongoClient("mongodb://localhost:27017")
db_name = "DuckPond"

# Connect to the database
db = mongo_client[db_name]

# Create an array of users
users = [BaseUser() for _ in range(NUM_OF_USERS)]

# Register all of the users to an account and login
for user in users:
    user.register()
    user.login()

all_post_ids = []
# Create each users posts
for user in users:
    for _ in range (NUM_OF_POSTS_PER_USER):
        user.create_post()
        all_post_ids.append(user.session_storage["current_post_id"])


# User interaction with posts
for post_id in all_post_ids:
    for user in users:
        if random() < USER_PROBABILITY_TO_LIKE:
            user.like_post(post_id)

        if random() < USER_PROBABILITY_TO_COMMENT:
            user.comment_on_post(post_id)


# Close the MongoDB connection
mongo_client.close()

print("Successfully populated MongoDB")
