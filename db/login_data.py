import pymongo
import os
from bson import ObjectId
from db import challenge_data

client = pymongo.MongoClient(os.environ.get('DB_URI'))
user_db = client['users']
login_col = user_db['login']


def is_valid_login(username):
  if login_col.find_one({'username': username.lower()}):
    return True

  return False


def id_by_username(username):
  return str(login_col.find_one({'username': username.lower()}, {'_id': 1})['_id'])


def username_by_id(id):
  return login_col.find_one({'_id': ObjectId(id)}, {'username': 1})['username']


def create_account(username):
  user_id = login_col.insert_one({'username': username.lower()}).inserted_id
  challenge_data.create_user_data(str(user_id))
