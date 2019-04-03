import time
import datetime
ss='49 分钟前'
s1='分钟前'
if ss.__contains__(s1):
	t=ss.split(s1)[0]
	# print(ss.split(s1)[0])
	# time
	# t=time.localtime().tm_hour-1
	print(t)
	# struct_time = time.strptime(time.time(), "%Y-%m-%d %H:%M:%S")
	print((datetime.datetime.now()-datetime.timedelta(minutes=int(t))).strftime("%Y-%m-%d %H:%M:%S"))
	# print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

