from flask import Blueprint, request, jsonify, render_template, make_response, session, redirect, g
from .models import *
from .helpers import generate_student_id, generate_receipt_no, remove_all_keys, change_date, get_date3
from app import login_required


clerk = Blueprint('clerk', __name__, url_prefix = '/clerk')

@clerk.route('/')
def home():
	return {'data': 'All is set'}

@clerk.route('/test_template')
@login_required
def test_template(current_user):
	name = "Sir Isaac Kwaku Newton"
	age = 30
	template = render_template('test_template.html', name=name, age=age)
	response = make_response(template)
	response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'
	return response

@clerk.route('/register_student', methods = ['POST'])
@login_required
def register_student(current_user):
	if request.method == 'POST':
		json_data = request.get_json()
		firstname = json_data.get('firstname')
		lastname = json_data.get('lastname')
		othername = json_data.get('othername')
		parent_phone = json_data.get('parent_phone')
		form = json_data.get('class')
		phone = json_data.get('phone')
		idx = generate_student_id(parent_phone, firstname)
		etl = [{'date': get_date3(datetime.utcnow()), 'amount':0}]
		pta = [{'date': get_date3(datetime.utcnow()), 'amount':0}]
		cha = [{'date': get_date3(datetime.utcnow()), 'etl':0, 'pta':0}]
		date_completed = "2022-1-2"
		try:
			add_student(firstname, lastname, othername, date_completed, form, parent_phone, phone, idx, g.user.get("fullname"), etl, pta, cha, status=1)
			return jsonify({'message':'success'}), 200
		except:
			return jsonify({'message': 'error'}), 500


@clerk.route('/pta_income', methods = ['POST'])
@login_required
def pta_income(current_user):
	if request.method == 'POST':
		json_data = request.get_json()
		mode = json_data.get('mode')
		number = json_data.get('number')
		semester = json_data.get('semester')
		amount = json_data.get('amount')
		student_id = json_data.get('student_id')
		name = json_data.get('name')
		form = json_data.get('form')
		if number:
			tx_id = number
		else:
			tx_id = 'taaghag'#generate_receipt_no()
		try:
			add_pta_income(clerk=g.user.get("fullname"), amount=amount, tx_id=tx_id, sem=semester, mode=mode, 
				cat='PTA', payer=student_id, name=name, form=form)
			student = get_one_student(student_id)
			idx = session.get('pay_id')
			new_data = {'date': get_date3(datetime.utcnow()), 'amount': amount}
			res = db.collection("main").document("students").collection('STD').document(idx).update({"pta_payment": firestore.ArrayUnion([new_data])})
			return jsonify({'message':'success', 'data': tx_id}), 200
		except:
			return jsonify({'message':'error'}), 500


@clerk.route('/etl_income', methods = ['POST'])
@login_required
def etl_income(current_user):
	if request.method == 'POST':
		json_data = request.get_json()
		mode = json_data.get('mode')
		number = json_data.get('number')
		semester = json_data.get('semester')
		amount = json_data.get('amount')
		student_id = json_data.get('student_id')
		name = json_data.get('name')
		form = json_data.get('form')
		if number:
			tx_id = number
		else:
			tx_id = 'taaghag'#generate_receipt_no()
		try:
			add_etl_income(clerk=g.user.get("fullname"), amount=amount, tx_id=tx_id, sem=semester, mode=mode, 
				cat='ETL', payer=student_id, name=name, form=form)
			student = get_one_student(student_id)
			idx = session.get('pay_id')
			new_data = {'date':get_date3(datetime.utcnow()), 'amount':amount}
			res = db.collection("main").document("students").collection('STD').document(idx).update({"etl_payment": firestore.ArrayUnion([new_data])})
			return jsonify({'message':'success', 'data': tx_id}), 200
		except:
			return jsonify({'message':'error'}), 500


@clerk.route('/donation_income', methods = ['POST'])
@login_required
def donation_income(current_user):
	if request.method == 'POST':
		json_data = request.get_json()
		name = json_data.get('name')
		mode = json_data.get('mode')
		semester = json_data.get('semester')
		amount = json_data.get('amount')
		phone = json_data.get('phone')
		tx_id = '172771'
		try:
			add_donation(clerk=g.user.get("fullname"), amount=amount, tx_id=tx_id, sem=semester, 
			mode=mode, cat='donation', phone=phone, name=name)
			add_pta_income(clerk=g.user.get("fullname"), amount=amount, tx_id=tx_id, sem=semester, mode=mode, cat='DON', payer=name,
			 name=name, form='PRV')
			return jsonify({'message':'success'}), 200
		except:
			return jsonify({'message':'error'}), 500

@clerk.route('/search_student', methods = ['POST'])
@login_required
def search_student(current_user):
	if request.method == 'POST':
		json_data = request.get_json()
		firstname = json_data.get('firstname')
		phone = json_data.get('parent_phone')
		stud_id = generate_student_id(phone, firstname)
		check = get_one_student(stud_id)
		if check:
			check = check.to_dict()
			data = {
			'firstname': check.get('firstname'),
			'lastname': check.get('lastname'),
			'form': check.get('form'),
			'p_phone': check.get('parent_phone'),
			'stud_id': check.get('student_id')
			}
			return jsonify({'message': 'success', 'data': data}), 200
		else:
			return jsonify({'message': 'error'}), 500

@clerk.route('/test', methods = ['POST', 'GET'])
@login_required
def test(current_user):
	if request.method == 'POST':
		json_data = request.get_json()
		print(json_data)
		return jsonify({'message': 'success'})
	return jsonify({'message': 'Get Data'})

@clerk.route('/dashboard_stats', methods = ['POST', 'GET'])
@login_required
def dashboard_stats(current_user):
	etl1 = get_etl_income_today()
	etl_amt = [float(res['amount']) for res in etl1]
	pta1 = get_pta_income_today()
	data1 = get_all_classes()
	form = sorted([res['class'] for res in data1])
	pta_amt = [float(res['amount']) for res in pta1]
	stud = get_all_students()
	data = {
		'pta': sum(pta_amt),
		'etl': sum(etl_amt),
		'students': len(stud)
			}
	template = render_template('clerk_dashboard.html', data=data, form=form)
	response = make_response(template)
	response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'
	return response, 200
	

@clerk.route('/pay_search_result', methods = ['POST', 'GET'])
@login_required
def pay_search_result(current_user):
	print(g.user)
	idx = session.get('pay_id')
	student = get_student_by_doc(idx)
	stud = {
		'firstname': student['firstname'],
		'lastname': student['lastname'],
		'form': student['form'],
		'phone': student['phone'],
		'idx': idx
	}
	template = render_template('pay_search_results.html', stud=stud)
	response = make_response(template)
	response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'
	return response, 200

@clerk.route('/get_pay_data', methods = ['POST'])
@login_required
def get_pay_data(current_user):
	if request.method == 'POST':
		data = request.get_json()
		session['pay_id'] = data['pay_id']
		return jsonify({'message': 'success'}), 200


@clerk.route('/student_pay', methods = ['POST', 'GET'])
@login_required
def student_pay(current_user):		
	form = request.args.get('form')
	list1 = student_list(form=form)
	template = render_template('student_pay.html', list1=list1, form=form)
	response = make_response(template)
	response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'
	return response, 200

@clerk.route('/daily_reports')
@login_required
def daily_reports(current_user):
	etl1 = get_etl_income_today()
	etl2 = [remove_all_keys(d,['semester', 'clerk', 'date']) for d in etl1]
	etl3 = [change_date(res) for res in etl2]
	etl3 = etl3[::-1]
	pta1 = get_pta_income_today()
	pta2 = [remove_all_keys(d,['semester', 'clerk', 'date']) for d in pta1]
	pta3 = [change_date(res) for res in pta2]
	pta3 = pta3[::-1]
	data = {
		'pta': pta3,
		'etl': etl3,
		
			}
	s1 = sum([float(i['amount']) for i in etl3])
	s2 = sum([float(i['amount']) for i in pta3])
	template = render_template('daily_report.html', data=data, etl_total=s1, pta_total=s2)
	response = make_response(template)
	response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'
	return response


@clerk.route('/get_student_classes')
@login_required
def get_student_classes(current_user):
	data = get_all_classes()
	data = [res['class'] for res in data]
	send = {'data': data}
	return jsonify(send), 200