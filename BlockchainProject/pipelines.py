# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymongo
from BlockchainProject.settings import mongodb_host, mongodb_db, mongodb_port, mongodb_coll_article_catalog, \
	mongodb_coll_article_body, mongodb_coll_article_img

from BlockchainProject.items import BlockchainprojectItem, ArticleBodyItem, ArticleImageItem


import requests


class BlockchainprojectPipeline(object):
	
	def __init__(self):
		host = mongodb_host
		port = mongodb_port
		db = mongodb_db
		# 文章列表集合
		coll_article_catalog = mongodb_coll_article_catalog
		# 文章内容集合
		coll_article_body = mongodb_coll_article_body
		# 文章图片集合
		coll_article_img = mongodb_coll_article_img
		
		# 连接mongodb
		client = pymongo.MongoClient(host=host, port=port)
		# 使用数据库
		blockobDb = client[db]
		# 使用文章列表集合
		self.coll_article_catalog = blockobDb[coll_article_catalog]
		self.coll_article_body = blockobDb[coll_article_body]
		self.coll_article_img = blockobDb[coll_article_img]
	
	def process_item(self, item, spider):
		if isinstance(item, BlockchainprojectItem):
			blockobItem = dict(item)
			if self.coll_article_catalog.find_one({'title': blockobItem['title']}):
				print("数据库中已存在")
			else:
				self.coll_article_catalog.insert(blockobItem)
			return item
		elif isinstance(item, ArticleBodyItem):
			# with open('D:\\blockob.txt', 'a', encoding='UTF-8') as f:
			# 	line = json.dumps(dict(item), ensure_ascii=False) + '\n'
			# 	f.write(line)
			
			artBodyItem = dict(item)
			if self.coll_article_body.find_one({'title': artBodyItem['title']}):
				print("数据库中已存在")
			else:
				self.coll_article_body.insert(artBodyItem)
		elif isinstance(item, ArticleImageItem):
			artImgItem = dict(item)
			if self.coll_article_img.find_one({'title': artImgItem['title']}):
				print("数据库中已存在")
			else:
				self.coll_article_img.insert(artImgItem)

