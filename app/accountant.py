from flask import Blueprint, request, jsonify, session, render_template, make_response,session, redirect, url_for, g
from .helpers import *
from .models import *
import datetime as dt
from itertools import accumulate
from app import login_required, date_formats, currency_format
import math as np

accountant = Blueprint('accountant', __name__, url_prefix = '/accountant')

report_data = {}
all_debtors = {}



@accountant.route('/reports', methods = ['POST'])
@login_required
def reports(current_user):
	if request.method == 'POST':
		json_data = request.get_json()
		start = json_data.get('start')
		end = json_data.get('end')
		kind = json_data.get('type')
		report = json_data.get('report')
		year = start[:4]
		month = start[5:7]
		day = start[8:]
		start1 = dt.datetime.strptime(start, "%Y-%m-%d").date()
		start = get_date2(start1)
		end1 = dt.datetime.strptime(end, "%Y-%m-%d").date()
		end = get_date2(end1)
		report_data['start'] = start
		report_data['end'] = end
		return redirect(url_for('accountant.etl_cash_receipt')), 200
		

@accountant.route('/todos', methods = ['POST'])
@login_required
def todos(current_user):
	if request.method == 'POST':
		json_data = request.get_json()
		task = json_data.get('task')
		return jsonify({'message':'success'})

@accountant.route('/search_ledger', methods = ['POST', 'GET'])
@login_required
def search_ledger(current_user):
	if request.method == 'POST':
		json_data = request.get_json()
		firstname = json_data.get('firstname')
		phone = json_data.get('parent_phone')
		stud_id = generate_student_id(phone, firstname)
		check = get_one_student(stud_id)
		if check:
			session['ledger_id'] = stud_id
			return redirect(url_for('accountant.ledger_results')), 200
		return jsonify({'message': 'error'}), 401
	template = render_template('search_ledger.html')
	response = make_response(template)
	response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'
	return response

@accountant.route('/ledger_results', methods=['GET', 'POST'])
@login_required
def ledger_results(current_user):
	doc_id = request.args.get('idx')
	form = request.args.get('form')
	student = student_ledger(doc_id, form)
	pta = student['pta_account']
	etl = student['etl_account']
	ptaa = [i['amount'] for i in pta]
	etll  = [i['amount'] for i in etl]

	print(etl)
	
	data = {
				'pta': pta,
				'etl': etl,
				'fullname': student.get('lastname') + " " + student.get('firstname'),
				'form': student.get('form'),
				'phone': student.get('parent_phone'),
				'pta_cum': list(accumulate(ptaa)),
				'etl_cum': list(accumulate(etll)),
				'etl_tot': sum([float(i['amount']) for i in etl]),
				'pta_tot': sum([float(i['amount']) for i in pta])
				}
	template = render_template('ledger_result.html', data=data)
	response = make_response(template)
	response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'
	return response
		
@accountant.route('/student_by_doc', methods = ['POST', 'GET'])
@login_required
def student_by_doc(current_user):		
	idx = request.args.get('idx')
	form = request.args.get('form')
	students = get_student_by_doc(idx, form)
	if type(students['dob']) == float:
		students['dob'] = get_date_back(students['dob'])
	return jsonify({'message': 'success', 'data': students})


@accountant.route('/debtors_list', methods = ['POST', 'GET'])
@login_required
def debtors_list(current_user):		
	form = request.args.get('form')
	#list1 = get_debtors_list(form=form)
	list1 = get_all_student_list(form=form)
	print(list1[0])
	
	pta_total = sum([i.get('pta_account_bal', 0) for i in list1 if not np.isnan(i.get('pta_account_bal', 0))])
	etl_total = sum([i.get('etl_account_bal', 0) for i in list1 if not np.isnan(i.get('etl_account_bal', 0))])
	list1 = sorted(list1, key=lambda x: x['lastname'])
	print(etl_total)
	template = render_template('debtors_list.html', list1=list1, form=form, pta_total=pta_total, etl_total=etl_total)
	response = make_response(template)
	response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'
	return response, 200
		
@accountant.route('/all_students', methods = ['POST', 'GET'])
@login_required
def all_students(current_user):		
	form = request.args.get('form')
	students = get_all_student_list(form=form)
	#print(students[0]['phone'])
	template = render_template('all_students.html', students=students, form=form)
	response = make_response(template)
	response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'
	return response, 200


@accountant.route('/show_all_debtors')
@login_required
def show_all_debtors(current_user):
	list1 = all_debtors
	return jsonify({'message': 'success', 'data': list1})


@accountant.route('/pta_expenses', methods = ['POST', 'GET'])
@login_required
def pta_expenses(current_user):
	if request.method == 'POST':
		json_data = request.get_json()
		details = json_data.get('details')
		category = json_data.get('category')
		sem = json_data.get('semester')
		mode = json_data.get('mode')
		quantity = json_data.get('quantity')
		amount = json_data.get('amount')
		try:
			add_pta_expense(clerk=g.user.get("fullname"), total=float(amount), detail=details, sem=sem, mode=mode, 
			quantity=quantity,cat=category)
			return jsonify({'message': 'success'}), 200
		except:
			return jsonify({'message': 'error'}), 500
	template = render_template('pta_expense_form.html')
	response = make_response(template)
	response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'
	return response


@accountant.route('/etl_expenses', methods = ['POST', 'GET'])
@login_required
def etl_expenses(current_user):
	if request.method == 'POST':
		json_data = request.get_json()
		details = json_data.get('details')
		category = json_data.get('category')
		sem = json_data.get('semester')
		mode = json_data.get('mode')
		quantity = json_data.get('quantity')
		amount = json_data.get('amount')
		try:
			add_etl_expense(clerk=g.user.get("fullname"), total=amount, detail=details, sem=sem, mode=mode, quantity=quantity,cat=category)
			return jsonify({'message': 'success'}), 200
		except:
			return jsonify({'message': 'error'}), 500
	template = render_template('etl_expense_form.html')
	response = make_response(template)
	response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'
	return response

@accountant.route('/add_category', methods = ['POST'])
@login_required
def add_category(current_user):
	if request.method == 'POST':
		json_data = request.get_json()
		category = json_data.get('category')
		if len(category) > 0:
			try:
				add_to_category(clerk = g.user.get("fullname"), category = category)
				return jsonify({'message': 'success'}), 200
			except:
				return jsonify({'message': 'error'}), 500
		else:
			return jsonify({'message': 'error'}), 400


@accountant.route('/send_categories')
@login_required
def send_categories(current_user):
	res = get_all_categories()
	res = [dat.get('category') for dat in res]
	return jsonify({'data': res})


@accountant.route('/add_class', methods = ['POST'])
@login_required
def add_class(current_user):
	if request.method == 'POST':
		json_data = request.get_json()
		form = json_data.get('form')
		if len(form) > 0:
			try:
				add_student_class(clerk = g.user.get("fullname"), form = form)
				return jsonify({'message': 'success'}), 200
			except:
				return jsonify({'message': 'error'}), 500
		else:
			return jsonify({'message': 'error'}), 400
	

@accountant.route('/begin_semester', methods = ['POST', 'GET'])
@login_required
def begin_semester(current_user):
	if request.method == 'POST':
		json_data = request.get_json()
		start = json_data.get('start')
		pta = json_data.get('pta')
		etl = json_data.get('etl')
		sem = json_data.get('sem')
		date = dt.date(year=int(start[:4]), month = int(start[5:7]), day = int(start[8:]))
		date2 = dt.datetime(int(start[:4]), int(start[5:7]), int(start[8:]), 0, 0)
		new_data = {'date':get_date3(date2), 'pta': etl, 'etl':pta}
		try:
			add_charge(clerk=g.user.get("fullname"), start=start, sem=sem, pta=pta, etl=etl)
			res = db.collection("main").document("students").collection('STD').get()
			ans = [update_doc(item=i, new_data=new_data) for i in res]
			return jsonify({'message': 'success'}), 200
		except:
			return jsonify({'message': 'error'}), 500
	template = render_template('begin_sem.html')
	response = make_response(template)
	response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'
	return response


def update_doc(item, new_data):
	id1 = item.id
	db.collection("main").document("students").collection('STD').document(id1).update({"charge": firestore.ArrayUnion([new_data])})

@accountant.route('/promote_students', methods = ['POST', 'GET'])
@login_required
def promote_students(current_user):
	if request.method == "POST":
		json_data = request.get_json()
		message = json_data.get('promote')
		if message == 'promote':
			try:
				promote_all_students()
				return jsonify({'message': 'success'}), 200
			except:
				return jsonify({'message': 'error1'})
		else:
			return jsonify({'message': 'error'}), 500
	return render_template("promote_students.html")


@accountant.route('/archive_student', methods = ['POST'])
@login_required
def archive_student(current_user):
	if request.method == "POST":
		json_data = request.get_json()
		message = json_data.get('message')
		if message == 'move':
			try:
				final = final_students()[0]
				return jsonify({'message': 'success', 'data': final})
			except:
				return jsonify({'message': 'error'})
		return jsonify({'message': 'error'})

	
@accountant.route('/other_business', methods = ['POST'])
@login_required
def other_business(current_user):
	if request.method == 'POST':
		json_data = request.get_json()
		start = json_data.get('start')
		end = json_data.get('end')
		amount = json_data.get('amount')
		name = json_data.get('name')
		details = json_data.get('details')
		try:
			add_other_income(clerk=g.user.get("fullname"), amount=amount, name=name, start=start, end=end, details=details)
			return jsonify({'message': 'success'}), 200
		except:
			return jsonify({'message': 'error'}), 400


@accountant.route('/pta_cash_receipt')
@login_required
def pta_cash_receipt(current_user):
	start = report_data.get('start')
	end = report_data.get('end')
	results = get_pta_cash_receipt(start, end)
	start = get_date_back(f1=start)
	end = get_date_back(f1=end)
	total1 = sum([float(i['amount']) for i in results if i['mode'] == 'Cash'])
	total2 = sum([float(i['amount']) for i in results if i['mode'] != 'Cash'])
	template = render_template('pta_cash_receipt.html', start=start, end=end, results=results, total1=total1, total2=total2)
	response = make_response(template)
	response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'
	return response

@accountant.route('/etl_cash_receipt')
@login_required
def etl_cash_receipt(current_user):
	start = report_data.get('start')
	end = report_data.get('end')
	results = get_etl_cash_receipt(start, end)
	start = get_date_back(f1=start)
	end = get_date_back(f1=end)
	total1 = sum([float(i['amount']) for i in results if i['mode'] == 'Cash'])
	total2 = sum([float(i['amount']) for i in results if i['mode'] != 'Cash'])
	template = render_template('etl_cash_receipt.html', start=start, end=end, results=results, total1=total1, total2=total2)
	response = make_response(template)
	response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'
	return response
	
@accountant.route('/etl_cash_payment')
@login_required
def etl_cash_payment(current_user):
	start = report_data.get('start')
	end = report_data.get('end')
	results = get_etl_cash_payment(start, end)
	start = get_date_back(f1=start)
	end = get_date_back(f1=end)
	total1 = sum([float(i['total']) for i in results if i['mode']=='CASH'])
	total2 = sum([float(i['total']) for i in results if i['mode']!='CASH'])
	template = render_template('etl_cash_payment.html', start=start, end=end, results=results, total1=total1, total2=total2)
	response = make_response(template)
	response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'
	return response

@accountant.route('/pta_cash_payment')
@login_required
def pta_cash_payment(current_user):
	start = report_data.get('start')
	end = report_data.get('end')
	results = get_pta_cash_payment(start, end)
	start = get_date_back(f1=start)
	end = get_date_back(f1=end)
	total1 = sum([float(i['total']) for i in results if i['mode']=='CASH'])
	total2 = sum([float(i['total']) for i in results if i['mode']!='CASH'])
	template = render_template('pta_cash_payment.html', start=start, end=end, results=results, total1=total1, total2=total2)
	response = make_response(template)
	response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'
	return response


@accountant.route('/etl_income_and_expenditure')
@login_required
def etl_income_and_expenditure(current_user):
	start = report_data.get('start')
	end = report_data.get('end')
	
	#Balance b/f

	dues0 = get_etl_cash_receipt_bal(start=start)
	dues0 = sum([float(i.get('amount')) for i in dues0])
	exxp = get_etl_cash_payment_bal(start=start)
	exp0 = sum([float(i.get('total')) for i in exxp])
	other0 = get_other_cash_receipt_bal(start=start)
	other0 = sum([float(i.get('amount')) for i in other0])
	profit0 = other0 + dues0 - exp0
	#Current data
	dues = get_etl_cash_receipt(start, end)
	dues1 = sum([float(i.get('amount')) for i in dues])
	other1 = get_other_cash_receipt(start=start, end=end)
	other1 = sum([float(i.get('amount')) for i in other1])
	exxp1 = get_etl_cash_payment(start=start, end=end)
	exp1 = sum([float(i.get('total')) for i in exxp1])
	
	cats = list(set([i['category'] for i in exxp1]))
	data = {val1: [i for i in res if i['category'] == val1] for val1 in cats}
	totals = {val1: sum([float(i['total']) for i in res if i['category'] == val1]) for val1 in cats}
	
	#Total
	total1 = dues1 + other1 + profit0
	profit1 = total1 - exp1
	start = get_date_back(f1=start)
	end = get_date_back(f1=end)
	template = render_template('etl_income_and_expenditure.html', start=start, end=end, dues1=dues1, other1=other1, total1=total1, profit0=profit0, profit1=profit1, data=data, totals=totals)
	response = make_response(template)
	response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'
	return response


@accountant.route('/pta_income_and_expenditure')
@login_required
def pta_income_and_expenditure(current_user):
	start = report_data.get('start')
	end = report_data.get('end')
	
	#Balance b/f

	dues0 = get_pta_cash_receipt_bal(start=start)
	dues0 = sum([float(i.get('amount')) for i in dues0])
	exxp = get_pta_cash_payment_bal(start=start)
	exp0 = sum([float(i.get('total')) for i in exxp])
	other0 = get_other_cash_receipt_bal(start=start)
	other0 = sum([float(i.get('amount')) for i in other0])
	profit0 = other0 + dues0 - exp0
	#Current data
	dues = get_pta_cash_receipt(start, end)
	dues1 = sum([float(i.get('amount')) for i in dues])
	other1 = get_other_cash_receipt(start=start, end=end)
	other1 = sum([float(i.get('amount')) for i in other1])
	exxp1 = get_pta_cash_payment(start=start, end=end)
	exp1 = sum([float(i.get('total')) for i in exxp1])
	
	cats = list(set([i['category'] for i in exxp1]))
	data = {val1: [i for i in res if i['category'] == val1] for val1 in cats}
	totals = {val1: sum([float(i['total']) for i in res if i['category'] == val1]) for val1 in cats}
	
	#Total
	total1 = dues1 + other1 + profit0
	profit1 = total1 - exp1
	start = get_date_back(f1=start)
	end = get_date_back(f1=end)
	template = render_template('pta_income_and_expenditure.html', start=start, end=end, dues1=dues1, other1=other1, total1=total1, profit0=profit0, profit1=profit1, data=data, totals=totals)
	response = make_response(template)
	response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'
	return response


@accountant.route('/dashboard_stats', methods = ['POST', 'GET'])
@login_required
def dashboard_stats(current_user):
	etl1 = get_etl_income_today()
	etl_amt = [float(res['amount']) for res in etl1]
	pta1 = get_pta_income_today()
	pta_amt = [float(res['amount']) for res in pta1]
	stud = get_all_students()
	data1 = get_all_classes()
	form = sorted([res['class'] for res in data1])
	template = render_template('accountant_dashboard.html', pta=sum(pta_amt), etl=sum(etl_amt), stud=len(stud), form=form)
	response = make_response(template)
	response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'
	return response

def change_date1(dict1):
	dict1['date'] = dict1['date'].date()
	return dict1


@accountant.route('/get_all_etl_expenses')
@login_required
def get_all_etl_expenses(current_user):
	data = get_etl_expenses()
	data1 = [change_date1(dat) for dat in data]
	send = {'data': data1}
	return jsonify(send), 200

@accountant.route('/get_all_pta_expenses')
@login_required
def get_all_pta_expenses(current_user):
	data = get_pta_expenses()
	data1 = [change_date(dat) for dat in data]
	send = {'data': data1}
	return jsonify(send), 200


@accountant.route('/daily_reports')
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
	data = {'pta': pta3, 'etl': etl3}
	s1 = sum([float(i['amount']) for i in etl3])
	s2 = sum([float(i['amount']) for i in pta3])
	template = render_template('daily_report.html', data=data, etl_total=s1, pta_total=s2)
	response = make_response(template)
	response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'
	return response

@accountant.route('/student_classes', methods = ['POST', 'GET'])
@login_required
def student_classes(current_user):
	data1 = get_all_classes()
	data = [res['class'] for res in data1]
	idx = [res['id'] for res in data1]
	data = [[k,v] for k,v in zip(idx, data)]
	send = {'data': data}
	template = render_template('student_classes.html', send=send)
	response = make_response(template)
	response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'
	return response

@accountant.route('/update_student_data', methods = ['POST'])
@login_required
def update_student_data(current_user):
	if request.method == 'POST':
		json_data = request.get_json()
		firstname = json_data.get('firstname')
		lastname = json_data.get('lastname')
		dob = json_data.get('dob')
		othername = json_data.get('othername')
		parent_phone = json_data.get('parent_phone')
		form = json_data.get('class')
		phone = json_data.get('phone')
		idx = generate_student_id(parent_phone, firstname)
		id1 = json_data.get('id')
		data = {
				'firstname': firstname,
				'lastname': lastname,
				'othername': othername,
				'form': form,
				'parent_phone': parent_phone,
				'phone': phone,
				'dob': dob,
				'student_id': idx,
				'class': form[0],
				}
		try:
			update_student(data, id1, form)
			return jsonify({'message': 'success'}), 200
		except:
			return jsonify({'message': 'failed'}), 500


@accountant.route('/delete_student', methods = ['POST', 'GET'])
@login_required
def delete_student(current_user):
	if request.method == 'POST':
		json_data = request.get_json()
		idx = json_data.get('id')
		form = json_data.get('form')
		delete_one_student(idx, form)
		return jsonify({'message': 'success'}), 200

@accountant.route('/delete_student_class', methods = ['POST'])
@login_required
def delete_student_class(current_user):
	if request.method == 'POST':
		cls_id = request.get_json()['id']
		delete_class(cls_id)
		return jsonify({'message': 'success'})


@accountant.route('/get_student_classes')
@login_required
def get_student_classes(current_user):
	data1 = get_all_classes()
	data = [res['class'] for res in data1]
	idx = [res['id'] for res in data1]
	data = [[k,v] for k,v in zip(idx, data)]
	
	send = {'data': data}
	return jsonify(send), 200


@accountant.route('/update_student_payment', methods = ['POST'])
@login_required
def update_student_payment(current_user):
	if request.method == 'POST':
		data = request.get_json()
		amt = float(data.get('amt'))
		form = data.get('form')
		loop = int(data.get('loop'))
		account = data.get('account')
		idx = data.get('idx')
		print(data)
		try:
			update_payment(amt, form, idx, loop, account)
			update_student_balance(form, idx, account)

			return jsonify({'message': 'success'}), 200
		except:
			return jsonify({'message': 'failed'}), 500

