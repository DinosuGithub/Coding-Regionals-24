import pymongo
import os
from bson import ObjectId
import challenges
from db import login_data

client = pymongo.MongoClient(os.environ.get('DB_URI'))
user_db = client['users']
challenge_col = user_db['challengeData']

def create_user_data(user_id):
  challenge_col.insert_one({'user_id': user_id, 'completed': [], 'scores': {}})

def completed_challenges(user_id):
  return challenge_col.find_one({'user_id': user_id}, {'completed': 1})['completed']


def incomplete_challenges(user_id):
  completed = completed_challenges(user_id)
  incomplete = []
  for challenge_num in range(1, len(challenges.challenges) + 1):
    if challenge_num not in completed:
      incomplete.append(challenge_num)
  
  return incomplete

def challenge_scores(user_id):
  return challenge_col.find_one({'user_id': user_id}, {'scores': 1})['scores']

def add_completed_challenge(user_id, challenge_num):
  completed = completed_challenges(user_id)
  
  if challenge_num not in completed:
    completed.append(challenge_num)
  
  challenge_col.update_one({'user_id': user_id}, {'$set': {'completed': completed}})

def update_user_score(user_id, challenge_num, score):
  scores = challenge_scores(user_id)

  scores[str(challenge_num)] = score
  
  challenge_col.update_one({'user_id': user_id}, {'$set': {'scores': scores}})

def challenge_score(user_id, challenge_num, default):
  scores = challenge_scores(user_id)

  score = default
  if str(challenge_num) in scores:
    score = scores[str(challenge_num)]

  return score

def challenge_leaderboard(challenge_num):
  data = []
  for user_data in challenge_col.find():
    if str(challenge_num) in user_data['scores'] and challenge_num in user_data['completed']:
      data.append({
        'username': login_data.username_by_id(user_data['user_id']),
        'score': user_data['scores'][str(challenge_num)]
      })

  data.sort(key=lambda user_data: user_data['score'])
  
  return data