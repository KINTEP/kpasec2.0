from flask import Blueprint, request, jsonify, redirect, url_for, render_template, session
from .models import *
from app import bcrypt
#import pyrebase


users = Blueprint('users', __name__, url_prefix = '/users')

#hash_password = bcrypt.generate_password_hash("kuminewton").decode("utf-8")
#add_staff(fullname="Kumi Newton", email="kuminewton@gmail.com", password=hash_password, role=2)

#firebaseConfig = {
#  "apiKey": "AIzaSyAbmZwfJBGdsiP6y5xGLIVXizI9G4kcpGY",
#  "authDomain": "kpasectrial.firebaseapp.com",
#  "projectId": "kpasectrial",
#  "storageBucket": "kpasectrial.appspot.com",
#  "messagingSenderId": "572488084748",
#  "appId": "1:572488084748:web:7faff7142e6aa15cb52d29"
#}


#firebase = pyrebase.initialize_app(firebaseConfig)
#auth = firebase.auth()

@users.route('/register_staff', methods = ['POST', 'GET'])
def register_staff():
	data = request.get_json()
	fullname = data.get('fullname')
	email = data.get('email')
	password = data.get('password')
	role = data.get('role')
	hash_password = bcrypt.generate_password_hash(password).decode("utf-8")
	try:
		add_staff(fullname=fullname, email=email, password=hash_password, role=role)
		return jsonify({'message': 'success'}), 200
	except:
		return jsonify({'message': 'error'}), 500


@users.route('/login_staff', methods = ['POST', 'GET'])
def login_staff():
	if request.method == 'POST':
		session.pop('user_id', None)
		email = request.form.get('email')
		password = request.form.get('password')
		staff = get_staff_by_email(email.lower())
		if staff:
			staff_id = staff[0].id
			staff_pass = staff[0].to_dict().get('password')
			if bcrypt.check_password_hash(staff_pass, password):
				session['user_id'] = staff_id
				role = staff[0].to_dict().get('role')
				session['role'] = role
				next_page = request.args.get('next')
				if role == 1:
					return redirect(next_page) if next_page else redirect(url_for('accountant.dashboard_stats'))
				if role == 2:
					return redirect(next_page) if next_page else redirect(url_for('clerk.dashboard_stats'))
			else:
				return redirect(url_for('users.login_staff'))
		else:
			return redirect(url_for('users.login_staff'))
	return render_template('login.html')


@users.route("/logout")
def logout():
	session.pop('user_id', None)
	return redirect(url_for('users.login_staff'))