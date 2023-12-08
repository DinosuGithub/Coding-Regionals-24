from flask import Flask, render_template, url_for, session, redirect, request, flash
from db import login_data
from db import challenge_data
import os
import challenges

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')


@app.before_request
def before_request():
  allowed_endpoints = ['static', 'home', 'login', 'signup']
  if 'user_id' not in session and request.endpoint not in allowed_endpoints:
    return redirect(url_for('login'))


@app.context_processor
def send_basic_info():
  all_challenges = [{'number': challenge_i + 1, 'name': challenge['name']} for challenge_i, challenge in enumerate(challenges.challenges)]
  
  session_username = ''
  completed_challenges = []
  
  if 'user_id' in session:
    user_id = session['user_id']
    session_username = login_data.username_by_id(user_id)
    completed_challenges = challenge_data.completed_challenges(user_id)

  return dict(username=session_username, all_challenges=all_challenges, completed_challenges=completed_challenges)


@app.route('/')
def home():
  if 'user_id' in session:
    return render_template('home.html')
  
  return render_template('welcome.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
  if 'user_id' in session:
    return redirect(url_for('home'))

  if request.method == 'GET':
    return render_template('login.html')
  elif request.method == 'POST':
    formUsername = request.form.get('username')

    if not login_data.is_valid_login(formUsername):
      flash(f'There is no existing account called called "{formUsername}."')
      return redirect(url_for('login'))

    session['user_id'] = login_data.id_by_username(formUsername)

    return redirect(url_for('home'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if 'user_id' in session:
    return redirect(url_for('home'))

  if request.method == 'GET':
    return render_template('signup.html')
  elif request.method == 'POST':
    formUsername = request.form.get('username')

    if login_data.is_valid_login(formUsername):
      flash(f'An account called "{formUsername}" already exists.')
      return redirect(url_for('signup'))

    login_data.create_account(formUsername)

    session['user_id'] = login_data.id_by_username(formUsername)

    return redirect(url_for('home'))


@app.route('/challenge/<int:challenge_num>')
def get_challenge(challenge_num):
  if challenge_num < 1:
    return 'Invalid URL. Challenge number must be at least 1.'
  
  completed = challenge_data.completed_challenges(session['user_id'])
  if challenge_num in completed:
    flash('You have already completed this challenge.')
  
  data = challenges.challenges[challenge_num - 1]
  return render_template('challenge.html', challenge_data={
    'num': challenge_num,
    'name': data['name'],
    'description': data['description'],
    'message': data['encode'](data['plaintext']),
    'hint': data['hint']
  })


@app.route('/challenge/<int:challenge_num>/submit', methods=['POST'])
def submit_challenge(challenge_num):
  submission = request.form.get('submission')
  
  challenge_info = challenges.challenges[challenge_num - 1]
  
  if submission.upper() == challenge_info['plaintext'].upper():
    challenge_data.add_completed_challenge(session['user_id'], challenge_num)
    return {'is_correct': True}
  
  return {'is_correct': False}


app.run(host='0.0.0.0', port=8080, debug=True)
