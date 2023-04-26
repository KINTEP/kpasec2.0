import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
from datetime import timedelta
from .helpers import *



data_to = {
	
  "type": "service_account",
  "project_id": "kpasec2",
  "private_key_id": "1218f19b379d2d8a536dd26ffeeafd890ec0e57c",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDHegKHVspemnN5\nLMW2rQdUawT1oVvtUUYddXREXb+2w6U646Wk11/PaqSfluWZvRrFSh69aFwAafzl\ncRCnWNdbqjh0c7sKzH/kQGGQUDGktOb2ajPldi/qPaFpJ8dX9FxnOV3OrL0EqDAL\nWmlSrxkUPCKI1ZM4TWj2zVZjpeNeSgj7BPGFeainGdHAQN6pcXKtRd+F0VuEe3bc\nNF8oc07WKOh47vUHEZo8pUmUE/sUIFq2n1O+h2ahu8SyweRqa0JO+gq+TY2rsvsm\njFP67ZoRCsMFf41rXFxvjXFn4tpKWQHHR2Mz2OeiaaZtVwP3v6fMEBjEXx5BO8ua\nYMzoeBT/AgMBAAECggEAYB1f/opJNFBDd42lLqIst/ZhC2HWg4D3wdYIUbDCYXPf\nt4JdHBJSrgR6khMJSoydy5YtPaJ9Qg3Pt1ZFaf0at6ZLUYE6DLgAn6CN4hVh9jTc\nXLtLijLqX3mWvq5WFQE/TNWNZ7o/0XCgxbeorBiGgwN+uGQAbc6O1uyVxan25kT3\niGHQVcVV+vOc1TxUvYqrj23FoHMIMX6156LXNiYb4YnfMdjOBkvobRS2EYJZnceD\nyjrohbxVT2GNGqVAredjJNVqq9uXdQDFr+ERELYQN5jEWKXQUiiIfG57bin/KcG1\nloi3vRslB0ZuRujgNv4hsdMJ+MUB24DkSu+vYB4pgQKBgQD1yeChAYcI0F8/Y4Vy\nxKVKAMlhGmxTD6QTreYD2wjVd62yKmqf74Z1wRClyoyzhXyEbdQbUChEJFKaUprr\n7I7JdOBBpn2stBr2kM/UmCCNpIbFiNe388zbl54GJlRu4K13xAah6slJpJzhfr2a\nhVxIZtaDZzCSyOeZWUi3Iw5DHwKBgQDPw5L79rY621Y55Iu8n5Xh3gI7qlj7H9dX\n+W1A2YJCcINYdI325Z8pJPDjGbPPTFlF703ZXUJUm+83q1laPEJy0ZFVgrUl0osb\nKly/UZ8TJ8b4TaJcqHiBwoZvg9v5yc+anRp408d/OvqgJfGjbbMXJaDd/Lvsmlbj\nsyBFPy7SIQKBgQCpvQfGyPJDMPuGICmJj6oCSDbKO2AxoGyUNpTRdtNL8EFg+A/4\ncYbvDSx9AjtWwsmx/tLrJdkY7eipsIBSi2Q0VeWFEQBbY2n3exw72e8pQkTcZ9tp\nqxF/WN6FqrTGeZzyR8q4yRbHJ8o7o7Y23wBS88oSpxGRXPMsIM+pwajYywKBgGgP\no/oRevqFy21ZvGewYsjrgqDR1JmLPDezFXaquuR+KDtQvZ5RKmPYPdLxl68XpYsy\nrgJWBJgONkXiy/E3R2zs7Gcw/XxBNS1ZDXVB83QLs0vAzrasJxePD/igybgVzaa6\nU3z7Teu65bb66kmZ815/mVA2ewWp1CVeHaaxW8khAoGAZP43HLKaYRyZ0bgHFeGN\nXEyS6p4zX2pcLyiZTUUwCuyth377olNqMHJyGnIaELjK7lXFZts6B5TRgsPFWtRK\nPa3nDnyVlZIbXUCrm9YJgE2jwOWoGbnQqLIha89YGVuI5BbiUc3TK1Pf5+TY/E1d\nh3e98bGoekGVA3AN9HvdpFM=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-lceyh@kpasec2.iam.gserviceaccount.com",
  "client_id": "102621528940948216766",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-lceyh%40kpasec2.iam.gserviceaccount.com"

}


cred = credentials.Certificate(data_to)
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

def add_student(firstname, lastname, othername, date_completed, form, parent_phone, phone, idx, clerk, etl, pta, cha, dob, status=1):
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
	'dob': dob,
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

def add_student22(fname, lname, oname, date11, form, pphone, phone, idx, clerk, etl, pta, dob, pta_bal, etl_bal, status=1):
    today = datetime.utcnow()
    stud = {
            'date': today, 'date2': get_date2(today), 'firstname': fname, 'lastname': lname,
            'othername': oname, 'form': form, 'parent_phone': pphone, 'phone': phone, 'dob': dob,
            'student_id': idx, 'class': form[0], 'status': status, 'date_completed': date11, 'etl_account': etl,
            'pta_account': pta, 'clerk': clerk,
            'pta_account_bal':pta_bal,
            'etl_account_bal':etl_bal,
            }
    
    db.collection("main").document("students").collection(f"form: {form[0]}").document(f"{form}").collection('STD').document().set(stud)

def add_pta_income(clerk, amount, tx_id, sem, mode, cat, payer, name, form, details, date):
	today = datetime.utcnow()
	pta = {
	'date': today,
	'date2': get_date22(date),
	'clerk': clerk,
	'amount': amount,
	'tx_id': tx_id,
	'semester': sem,
	'mode': mode,
	'category': cat,
	'payer': payer,
	'name': name,
	'class': form,
	'details': details
		}
	db.collection("main").document("pta_income").collection('PTA').document().set(pta)


def add_etl_income(clerk, amount, tx_id, sem, mode, cat, payer, name, form, details, date):
	today = datetime.utcnow()
	etl = {
	'date': today,
	'date2': get_date22(date),
	'clerk': clerk,
	'amount': amount,
	'tx_id': tx_id,
	'semester': sem,
	'mode': mode,
	'category': cat,
	'payer': payer,
	'name': name,
	'class': form,
	'details':details
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

def get_student_by_doc(idx, form):
	#results = db.collection("main").document("students").collection('STD').document(idx).get()
	results = db.collection("main").document("students").collection(f"form: {form[0]}").document(f"{form}").collection('STD').document(idx).get()
	return results.to_dict()


def get_all_classes():
	result = db.collection("main").document("student_classes").collection('CLS').order_by("class", direction=firestore.Query.DESCENDING).get()
	data = [add_ids(res.to_dict(), res.id) for res in result]
	return data[::-1]

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

def get_one_student(idx, form):
	#stud = db.collection("main").document("students").collection('STD').where("student_id", "==", idx).get()
	stud = db.collection("main").document("students").collection('STD').document(f"{form}").collection('STD').where("student_id", "==", idx).get()
	if stud:
		return stud[0]
	return False

def student_ledger(idx, form):
	stud = get_student_by_doc(idx, form)
	if stud:
		stud = stud
		return stud
	else:
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

def get_etl_cash_receipt_bal(start):
	res = db.collection("main").document("etl_income").collection('ETL').where("date2", "<", start).get()
	res2 = [i.to_dict() for i in res]
	return res2

def get_pta_cash_receipt_bal(start):
	res = db.collection("main").document("etl_income").collection('ETL').where("date2", "<", start).get()
	res2 = [i.to_dict() for i in res]
	return res2

def get_pta_cash_receipt(start, end):
	res = db.collection("main").document("pta_income").collection('PTA').where("date2", ">=", start).where("date2", "<=", end).get()
	res2 = [i.to_dict() for i in res]
	return res2

def get_other_cash_receipt(start, end):
	res = db.collection("main").document("other_income").collection('OTH').where("date2", ">=", start).where("date2", "<=", end).get()
	res2 = [i.to_dict() for i in res]
	return res2

def get_other_cash_receipt_bal(start):
	res = db.collection("main").document("other_income").collection('OTH').where("date2", "<", start).get()
	res2 = [i.to_dict() for i in res]
	return res2

#db.collection("main").document("other_income").collection('OTH').document().set(oth)

def get_etl_cash_payment(start, end):
	res = db.collection("main").document("etl_expense").collection('ETL').where("date2", ">=", start).where("date2", "<=", end).get()
	res2 = [i.to_dict() for i in res]
	return res2

def get_pta_cash_payment(start, end):
	res = db.collection("main").document("pta_expense").collection('PTA').where("date2", ">=", start).where("date2", "<=", end).get()
	res2 = [i.to_dict() for i in res]
	return res2

def get_pta_cash_payment_bal(start):
	res = db.collection("main").document("pta_expense").collection('PTA').where("date2", "<", start).get()
	res2 = [i.to_dict() for i in res]
	return res2

def get_etl_cash_payment_bal(start):
	res = db.collection("main").document("etl_expense").collection('ETL').where("date2", "<", start).get()
	res2 = [i.to_dict() for i in res]
	return res2

def get_debtors_list(form):
	#results = db.collection("main").document("students").collection('STD').where('form', '==', form).get()
	results = db.collection("main").document("students").collection('STD').document(f"{form}").collection('STD').get()
	#print(results[0].to_dict())
	obj = [add_ids(res.to_dict(), res.id) for res in results]
	#print(obj[0])
	all_list = [get_balance(obj=i) for i in obj]
	return all_list

def get_all_student_list(form):
	result = db.collection("main").document("students").collection(f"form: {form[0]}").document(f"{form}").collection('STD').get()
	#print(result)
	data = [add_ids(res.to_dict(), res.id) for res in result]
	return data

#P1 = get_all_student_list(form='3G3')
#print(P1[0])
def get_student_balance(idx, form):
    res = db.collection("main").document("students").collection(f"form: {form[0]}").document(f"{form}").collection('STD').document(idx)
    results = res.get()
    ans = results.to_dict()
    etl = ans['etl_account'][-1]['balance']
    pta = ans['pta_account'][-1]['balance']
    return etl, pta



def student_list(form):
	#result = db.collection("main").document("students").collection('STD').where('form', '==', form).get()
	#result = db.collection("main").document("students").collection('STD').document(f"{form}").collection('STD').get()
	#results = db.collection("main").document("students").collection('STD').document(f"{form}").collection('STD').get()
	results = db.collection("main").document("students").collection(f"form: {form[0]}").document(f"{form}").collection('STD').get()
	#print(results)
	#obj = [i.to_dict() for i in res]
	data = [add_ids(res.to_dict(), res.id) for res in results]
	return data

def get_balance(obj):
	idx = obj.get('student_id')
	idx1 = obj.get('id')
	form = obj.get('form')
	stud = get_one_student(idx, form)
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
			'etl': etl_bal,
			'id': idx1
		}
		return data
	return False

def get_balance2(idx, form):
	#stud = get_one_student(idx, form)
	stud = get_student_by_doc(idx, form)
	#print(stud)
	#if stud:
	#stud = stud.to_dict()
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
			'pta_balance': pta_bal,
			'etl_balance': etl_bal,
		}
	return data


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


def promote_all_students2():
	ref = db.collection("main").document("students").collection(f"form: {form[0]}").document(f"{form}").collection('STD').document().set(stud)

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





def update_student_balance(form, idx, account='etl_account'):
    res = db.collection("main").document("students").collection(f"form: {form[0]}").document(f"{form}").collection('STD').document(idx)
    results = res.get()
    ans = results.to_dict()
    acc = ans[account]
    amt = [i['amount'] for i in acc]
    res.update({account+"_bal": sum(amt)})



####
def update_payment(amt, form, idx, loop, account):
    res = db.collection("main").document("students").collection(f"form: {form[0]}").document(f"{form}").collection('STD').document(idx)
    results = res.get()
    ans = results.to_dict()
    payments = ans[account]
    for a,b in enumerate(payments):
        if a == loop:
            b['amount'] = amt
    res.update({account: payments})


def update_student(data, idx, form):
	#db.collection("main").document("students").collection('STD').document(idx).update(data)
	db.collection("main").document("students").collection(f"form: {form[0]}").document(f"{form}").collection('STD').document(idx).update(data)


def delete_one_student(idx, form):
	#db.collection("main").document("students").collection('STD').document(idx).delete()
	db.collection("main").document("students").collection(f"form: {form[0]}").document(f"{form}").collection('STD').document(idx).delete()



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
