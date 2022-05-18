import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
from datetime import timedelta
from .helpers import *



cred = credentials.Certificate(r"app/trial1.json")
firebase_admin.initialize_app(cred)

db = firestore.client()



def add_staff(fullname, email, password, role):
	today = datetime.utcnow()
	user = {
	
	'date': today,
	'date2': get_date2(today),
	'fullname': fullname,
	'email': email,
	'password': password,
	'role': role
		}
	db.collection("main").document("staff").collection('STF').document().set(user)

def add_student_archives(stud):
	db.collection("main").document("student_archives").collection('STD').document().set(stud)

def add_student(firstname, lastname, othername, date_completed, form, parent_phone, phone, idx, clerk, etl, pta, cha, status=1):
	today = datetime.utcnow()
	stud = {
	'date': today,
	'date2': get_date2(today),
	'firstname': firstname,
	'lastname': lastname,
	'othername': othername,
	'form': form,
	'parent_phone': parent_phone,
	'phone': phone,
	'student_id': idx,
	'class': form[0],
	'status': status,
	'date_completed': date_completed,
	'etl_payment': etl,
	'pta_payment': pta,
	'charge': cha,
	'clerk': clerk
		}
	db.collection("main").document("students").collection('STD').document().set(stud)


def add_pta_income(clerk, amount, tx_id, sem, mode, cat, payer, name, form):
	today = datetime.utcnow()
	pta = {
	'date': today,
	'date2': get_date2(today),
	'clerk': clerk,
	'amount': amount,
	'tx_id': tx_id,
	'semester': sem,
	'mode': mode,
	'category': cat,
	'payer': payer,
	'name': name,
	'class': form
		}
	db.collection("main").document("pta_income").collection('PTA').document().set(pta)


def add_etl_income(clerk, amount, tx_id, sem, mode, cat, payer, name, form):
	today = datetime.utcnow()
	etl = {
	'date': today,
	'date2': get_date2(today),
	'clerk': clerk,
	'amount': amount,
	'tx_id': tx_id,
	'semester': sem,
	'mode': mode,
	'category': cat,
	'payer': payer,
	'name': name,
	'class': form
		}
	db.collection("main").document("etl_income").collection('ETL').document().set(etl)


def add_other_income(clerk, amount, name, start, end, details):
	today = datetime.utcnow()
	oth = {
	'date': today,
	'date2': get_date2(today),
	'clerk': clerk,
	'amount': amount,
	'name': name,
	'start': start,
	'end': end,
	'details': details
		}
	db.collection("main").document("other_income").collection('OTH').document().set(oth)



def add_pta_expense(clerk, total, detail, sem, mode, quantity, cat):
	today = datetime.utcnow()
	pta = {
	'date': today,
	'date2': get_date2(today),
	'clerk': clerk,
	'detail': detail,
	'semester': sem,
	'mode': mode,
	'category': cat,
	'quantity': quantity,
	'total': total
		}
	db.collection("main").document("pta_expense").collection('PTA').document().set(pta)


def add_etl_expense(clerk, total, detail, sem, mode, quantity,cat):
	today = datetime.utcnow()
	etl = {
	'date': today,
	'date2': get_date2(today),
	'clerk': clerk,
	'detail': detail,
	'semester': sem,
	'mode': mode,
	'category': cat,
	'quantity': quantity,
	'total': total
		}
	db.collection("main").document("etl_expense").collection('ETL').document().set(etl)


def add_charge(clerk, start, sem, pta, etl):
	today = datetime.utcnow()
	ch = {
	'date': today,
	'date2': get_date2(today),
	'clerk': clerk,
	'start': start,
	'semester': sem,
	'etl': float(etl),
	'pta': float(pta),
	'total': float(etl) + float(pta)
		}
	db.collection("main").document("charges").collection('CHG').document().set(ch)


def add_to_category(clerk, category):
	today = datetime.utcnow()
	cat = {
	'date': today,
	'date2': get_date2(today),
	'clerk': clerk,
	'category': category
		}
	db.collection("main").document("expense_category").collection('CAT').document().set(cat)



def add_student_class(clerk, form):
	today = datetime.utcnow()
	cls1 = {
	'date': today,
	'date2': get_date2(today),
	'clerk': clerk,
	'class': form
		}
	db.collection("main").document("student_classes").collection('CLS').document().set(cls1)


def add_donation(clerk, amount, tx_id, sem, mode, cat, phone, name):
	today = datetime.utcnow()
	don = {
	'date': today,
	'date2': get_date2(today),
	'clerk': clerk,
	'amount': amount,
	'tx_id': tx_id,
	'semester': sem,
	'mode': mode,
	'category': cat,
	'phone': phone,
	'name': name
		}
	db.collection("main").document("donations").collection('PTA').document().set(don)









####

def get_student_by_doc(idx):
	results = db.collection("main").document("students").collection('STD').document(idx).get()
	return results.to_dict()


def get_all_classes():
	result = db.collection("main").document("student_classes").collection('CLS').order_by("date", direction=firestore.Query.DESCENDING).get()
	data = [add_ids(res.to_dict(), res.id) for res in result]
	return data

def get_all_categories():
	results = db.collection("main").document("expense_category").collection('CAT').get()
	data = [res.to_dict() for res in results]
	return data


def get_etl_expenses():
	results = db.collection("main").document("etl_expense").collection('ETL').get()
	data = [res.to_dict() for res in results]
	return data

def get_pta_expenses():
	results = db.collection("main").document("pta_expense").collection('PTA').get()
	data = [res.to_dict() for res in results]
	return data

def get_one_student(idx):
	stud = db.collection("main").document("students").collection('STD').where("student_id", "==", idx).get()
	if stud:
			return stud[0]
	return False

def student_ledger(idx):
	stud = get_one_student(idx)
	if stud:
		stud = stud.to_dict()
		etl_pmt = stud['etl_payment']
		pta_pmt = stud['pta_payment']
		if type(etl_pmt) == list:
			etl_pmt = [change_category(dict1=d1, kind='etl') for d1 in etl_pmt]
		else:
			etl_pmt = [change_category(dict1=etl_pmt, kind='etl')]
		
		if type(pta_pmt) != list:
			pta_pmt = [change_category(stud['pta_payment'], kind='pta')]
		else:
			pta_pmt = [change_category(dict1=d1, kind='pta') for d1 in pta_pmt]
		charge = stud['charge']
		etll = [get_right_data(dict1=d1, kind='etl') for d1 in charge]
		ptaa = [get_right_data(dict1=d1, kind='pta') for d1 in charge]
		etll += etl_pmt[:]
		ptaa += pta_pmt[:]
		etll = sort_list_dict(etll, 'date')
		ptaa = sort_list_dict(ptaa, 'date')
		etll = [get_all_dates_back(dict1=i) for i in etll]
		ptaa = [get_all_dates_back(dict1=i) for i in ptaa]
		return etll, ptaa
	return False

def get_right_data(dict1, kind='etl'):
	new_dict = {}
	new_dict['date'] = dict1['date']
	if kind == 'etl':
		new_dict['amount'] = dict1['etl']
		new_dict['cat'] = 'cha'
	if kind == 'pta':
		new_dict['amount'] = dict1['pta']
		new_dict['cat'] = 'cha'
	return new_dict

def change_category(dict1, kind='etl'):
	dict1['cat'] = kind
	return dict1


def get_all_students():
	result = db.collection("main").document("students").collection('STD').get()
	res1 = [res.to_dict() for res in result]
	return res1

def get_etl_income_today():
	today = datetime.utcnow()
	date = get_date2(today)
	res = db.collection("main").document("etl_income").collection('ETL').where("date2", "==", date).get()
	res = [i.to_dict() for i in res]
	res = sort_list_dict(res, 'date')
	return res

def get_pta_income_today():
	today = datetime.utcnow()
	date = get_date2(today)
	res = db.collection("main").document("pta_income").collection('PTA').where("date2", "==", date).get()
	res = [i.to_dict() for i in res]
	res = sort_list_dict(res, 'date')
	return res

def get_etl_cash_receipt(start, end):
	res = db.collection("main").document("etl_income").collection('ETL').where("date2", ">=", start).where("date2", "<=", end).get()
	res2 = [i.to_dict() for i in res]
	return res2

def get_pta_cash_receipt(start, end):
	res = db.collection("main").document("pta_income").collection('PTA').where("date2", ">=", start).where("date2", "<=", end).get()
	res2 = [i.to_dict() for i in res]
	return res2


def get_etl_cash_payment(start, end):
	res = db.collection("main").document("etl_expense").collection('ETL').where("date2", ">=", start).where("date2", "<=", end).get()
	res2 = [i.to_dict() for i in res]
	return res2

def get_pta_cash_payment(start, end):
	res = db.collection("main").document("pta_expense").collection('PTA').where("date2", ">=", start).where("date2", "<=", end).get()
	res2 = [i.to_dict() for i in res]
	return res2

def get_debtors_list(form):
	res = db.collection("main").document("students").collection('STD').where('form', '==', form).get()
	obj = [i.to_dict() for i in res]
	all_list = [get_balance(obj=i) for i in obj]
	return all_list

def student_list(form):
	result = db.collection("main").document("students").collection('STD').where('form', '==', form).get()
	#obj = [i.to_dict() for i in res]
	data = [add_ids(res.to_dict(), res.id) for res in result]
	return data

def get_balance(obj):
	idx = obj.get('student_id')
	stud = get_one_student(idx)
	if stud:
		stud = stud.to_dict()
		etl_pmt = stud['etl_payment'][:]
		pta_pmt = stud['pta_payment'][:]
		pta = [float(i['amount']) for i in pta_pmt]
		etl = [float(i['amount']) for i in etl_pmt]
		charge = stud['charge'][:]
		pta_char = [float(i['pta']) for i in charge]
		etl_char = [float(i['etl']) for i in charge]
		pta_bal = -sum(pta_char) + sum(pta)
		etl_bal = -sum(etl_char) + sum(etl)
		data = {
			'form': stud['form'],
			'name': stud['firstname'] + " " + stud['lastname'],
			'pta': pta_bal,
			'etl': etl_bal
		}
		return data
	return False


def promote_all_students():
	res = db.collection("main").document("students").collection('STD').get()
	idxs = [i.id for i in res]
	dict_data = [i.to_dict() for i in res]
	for i in range(len(res)):
		form = dict_data[i]['form']
		new_cls = promote_student(form)
		if new_cls:
			idx = idxs[i]
			db.collection("main").document("students").collection('STD').document(idx).update({"form": new_cls, "class": new_cls[0]})

##


def get_staff_by_email(email):
	res = db.collection("main").document("staff").collection('STF').where('email', '==', email).get()
	return res


def get_user(user_id):
	res = db.collection("main").document("staff").collection('STF').document(user_id).get()
	return res

#print(get_user("VJb1U9tevEZ5SZxjK8G1").to_dict())
#res = get_staff_by_email(email="kuminewton@gmail.com")
#print(res[0].to_dict())






####
def delete_class(cls_id):
	db.collection("main").document("student_classes").collection('CLS').document(cls_id).delete()

def final_students(form=3):
	stud = db.collection("main").document("students").collection('STD').where("class", "==", str(form)).get()
	idxs = [i.id for i in stud]
	data = [i.to_dict() for i in stud]
	[add_student_archives(i) for i in data]
	[db.collection("main").document("students").collection('STD').document(i).delete() for i in idxs]
	return len(stud), True

##print()
