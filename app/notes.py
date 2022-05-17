import datetime
import time
 
# assigned regular string date
date_time = datetime.datetime(2021, 7, 26, 21, 20)
 
# print regular python date&time
print("date_time =>",date_time)
 
# displaying unix timestamp after conversion
print("unix_timestamp => ",
      (time.mktime(date_time.timetuple())))


# assigned unix time
unix_time = 1627334400
 
date_time = datetime.datetime.fromtimestamp(unix_time)
 
# print unix time stamp
print("Unix_Time =>",unix_time)
 
# displaying date and time in a regular
# string format
print("Date & Time =>" , date_time.strftime('%Y-%m-%d %H:%M:%S'))