import datetime as dt
from datetime import datetime as df
import math
import time

def generate_student_id(contact, firstname):
    firstname = str(firstname).lower()
    res = str(contact) + firstname
    return res

def promote_student(current_class):
    index = int(current_class[0])
    if index < 3:
        index += 1
        return str(index) + current_class[1:]
    else:
        return False

#print(promote_student(current_class='3A3'))

def add_ids(dict1, idx):
    dict1['id'] = idx
    return dict1

def sort_list_dict(lis, key):
    ls = sorted(lis, key = lambda i: i[key])
    return ls

def get_date3(date1):
    date2 = time.mktime(date1.timetuple())
    return date2

def get_date2(today):
    year = today.year
    month = today.month
    day = today.day
    date = df(year, month, day)
    date2 = time.mktime(date.timetuple())
    return date2

def get_all_dates_back(dict1):
    dict1['date'] = get_date_back(dict1['date'])
    return dict1

def get_date_back(f1):
    date_time = dt.datetime.fromtimestamp(f1)
    return str(date_time.date())

def change_date(dict1):
    dict1['date2'] = get_date_back(dict1['date2'])
    return dict1

def remove_key(dict1, key):
    dict1.pop(key)
    return dict1

def remove_all_keys(dict1, keys):
    res = [remove_key(dict1, key=key) for key in keys]
    return dict1

def generate_receipt_no():
    today = dt.datetime.now()
    if today.month == 1 and today.day == 1:
        name = f"nums{today.year}.txt"
        newf = open(name, "a")
    y1 = str(dt.datetime.now().year) + str(dt.datetime.now().month)
    name = r"C:/Users/user/Desktop/kpasec201/app/number.txt"
    rand = math.random.randint(10000, 100000)
    newf = open(name, "a")
    file = open(name, "r")
    idx = y1+str(rand)
    read = file.read()
    file.close()
    if idx not in read:
        with open(name, "a") as f1:
            f1.write(f"{idx}\n")
        return idx