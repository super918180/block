import pymongo
import time
import jieba.analyse
from pymongo import MongoClient
client=MongoClient('127.0.0.1',27017)
db=client['blockchain']
coll_article_catalog=db['article_catalogs']
coll_keywords=db['keywords']
titleList=[]
for i in coll_article_catalog.find({}):
	titleList.append(i['title'])
titleStr=",".join(titleList)
print(titleStr)
dict={}
for k, v in jieba.analyse.textrank(titleStr, withWeight=True, topK=100):
		dict[k]=v
		print('%s,%s' % (k, v))
time=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
coll_keywords.insert_one({"keywords":dict,'createTime':time})