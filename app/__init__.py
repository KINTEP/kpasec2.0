from flask import Flask, jsonify, session, redirect, url_for, g
from flask_cors import CORS
import os
from functools import wraps
from flask_bcrypt import Bcrypt
from app.models import get_user
from datetime import timedelta

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = '617657yaghjaghaj'
CORS(app)


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=200)
    if "user_id" in session:
    	user_id = session.get('user_id')
    	user = get_user(user_id)
    	g.user = user.to_dict()

def login_required(f):
	@wraps(f)
	def decorated(*args, **kwags):
		user_id = None
		if "user_id" in session:
			user_id = session.get('user_id')
		if not user_id:
			return redirect(url_for('users.login_staff'))
		try:
			current_user = get_user(user_id)
		except:
			return jsonify({'message': 'InvalidUser'}), 401
		return f(current_user, *args, **kwags)
	return decorated


@app.route('/')
@login_required
def index(current_user):
	return jsonify({'data': 'All is good'})



from app.users import users
from app.clerk import clerk
from app.accountant import accountant

app.register_blueprint(clerk)
app.register_blueprint(users)
app.register_blueprint(accountant)

