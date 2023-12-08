import pymongo
import os
from bson import ObjectId

client = pymongo.MongoClient(os.environ.get('DB_URI'))
user_db = client['users']
challenge_col = user_db['challengeData']

def create_user_data(user_id):
  challenge_col.insert_one({'user_id': user_id, 'completed': []})

def completed_challenges(user_id):
  return challenge_col.find_one({'user_id': user_id}, {'completed': 1})['completed']

def add_completed_challenge(user_id, challenge_num):
  completed = challenge_col.find_one({'user_id': user_id}, {'completed': 1})['completed']
  
  if challenge_num not in completed:
    completed.append(challenge_num)
  
  challenge_col.update_one({'user_id': user_id}, {'$set': {'completed': completed}})
