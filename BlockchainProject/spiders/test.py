tag = 1
dic = {}
list=[{1:'a'},{2:'s'}]
# for i in range(10):
# 	dic[tag] = tag
# 	tag += 1
# list.append(dict)
ss=''
for i in range(len(list)):
	d=list[i]
	for k,v in d.items():
		ss=ss+''.join(v)
print(ss)