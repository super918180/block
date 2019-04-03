# -*- coding: utf-8 -*-

import scrapy
from BlockchainProject.items import BlockchainprojectItem, ArticleBodyItem, ArticleImageItem
import re
import json
from scrapy.selector import Selector
import requests
from bson import binary
import datetime

class BlockobSpider(scrapy.Spider):
	name = 'blockob'
	allowed_domains = ['www.blockob.com']
	start_urls = ['https://www.blockob.com']
	searchEndTime = '2019-03-01'
	timeReg = '小时前'
	
	def parse(self, response):
		recommendArticleList = response.xpath(
			'//div[@id="articles"]//div[@class="tab_content"][1]//div[@class="tab_cont"]//div[@class="post_item clearfix"]')
		policyArticleList = response.xpath(
			'//div[@id="articles"]//div[@class="tab_content"][2]//div[@class="tab_cont"]//div[@class="post_item clearfix"]')
		# 爬取推荐文章
		for i_item in recommendArticleList:
			remArticleItem = BlockchainprojectItem()
			remArticleItem['type'] = 'recommend'
			remArticleItem['title'] = i_item.xpath(
				'.//h4[@class="post_tit"]/a[@target="_blank"]/text()').extract_first()
			remArticleItem['introduce'] = i_item.xpath('.//div[@class="post_profile"]/text()').extract_first()
			remArticleItem['artUrl'] = BlockobSpider.start_urls[0] + i_item.xpath(
				'.//h4[@class="post_tit"]/a[@target="_blank"]/@href').extract_first()
			remArticleItem['sourceUrl'] = BlockobSpider.start_urls[0] + i_item.xpath(
				'.//div[@class="post_meta"]/a[@class="post_author"]/@href').extract_first()
			artTime= \
				i_item.xpath('.//div[@class="post_meta"]/span[@class="post_date"]/text()').extract()[0].split()[1]
			if artTime.__contains__(self.timeReg):
				th=artTime.split(self.timeReg)[0];
				remArticleItem['artTime']=(datetime.datetime.now()-datetime.timedelta(hours=int(th))).strftime("%Y-%m-%d %H:%M:%S")
			else:
				remArticleItem['artTime']=artTime;
			if remArticleItem['artTime'] >= self.searchEndTime:
				yield remArticleItem
				if remArticleItem['artUrl']:
					remArtUrl = remArticleItem['artUrl']
					yield scrapy.Request(remArtUrl, callback=self.parse_detail)
				if remArtUrl:
					remId = re.findall(r'/posts/info/([0-9]+)', remArtUrl)
		# print(articleItem)
		if remId:
			remNext_link = "https://www.blockob.com/posts/get-recommend-list?id=" + remId[0]
			print("next_link", remNext_link)
			yield scrapy.Request(remNext_link, callback=self.parse_loadmore_recommend)
		# 爬取政策文章
		for i_item in policyArticleList:
			polArticleItem = BlockchainprojectItem()
			polArticleItem['type'] = 'policy'
			polArticleItem['title'] = i_item.xpath(
				'.//h4[@class="post_tit"]/a[@target="_blank"]/text()').extract_first()
			polArticleItem['introduce'] = i_item.xpath('.//div[@class="post_profile"]/text()').extract_first()
			polArticleItem['artUrl'] = BlockobSpider.start_urls[0] + i_item.xpath(
				'.//h4[@class="post_tit"]/a[@target="_blank"]/@href').extract_first()
			polArticleItem['sourceUrl'] = BlockobSpider.start_urls[0] + i_item.xpath(
				'.//div[@class="post_meta"]/a[@class="post_author"]/@href').extract_first()
			artTime = \
				i_item.xpath('.//div[@class="post_meta"]/span[@class="post_date"]/text()').extract()[0].split()[1]
			if artTime.__contains__(self.timeReg):
				th = artTime.split(self.timeReg)[0];
				polArticleItem['artTime'] = (datetime.datetime.now() - datetime.timedelta(hours=int(th))).strftime(
					"%Y-%m-%d %H:%M:%S")
			else:
				polArticleItem['artTime']=artTime
			if polArticleItem['artTime'] >= self.searchEndTime:
				yield polArticleItem
				if polArticleItem['artUrl']:
					polArtUrl = polArticleItem['artUrl']
					yield scrapy.Request(polArtUrl, callback=self.parse_detail)
				if polArtUrl:
					polId = re.findall(r'/posts/info/([0-9]+)', polArtUrl)
		# print(articleItem)
		if polId:
			polNext_link = "https://www.blockob.com/posts/get-list-by-term-id?term_id=4&id=" + polId[0]
			print("next_link", polNext_link)
			yield scrapy.Request(polNext_link, callback=self.parse_loadmore_policy)
	
	# 解析更多的推荐文章
	def parse_loadmore_recommend(self, response):
		if response.text.__contains__("code"):
			data = json.loads(response.text)
			response = data['data']
		# print(response)
		articleList = Selector(text=response).xpath(
			'//div[@class="post_item clearfix"]')
		# print(articleList)
		for i_item in articleList:
			articleItem = BlockchainprojectItem()
			articleItem['title'] = i_item.xpath('.//h4[@class="post_tit"]/a[@target="_blank"]/text()').extract_first()
			articleItem['introduce'] = i_item.xpath('.//div[@class="post_profile"]/text()').extract_first()
			articleItem['artUrl'] = BlockobSpider.start_urls[0] + i_item.xpath(
				'.//h4[@class="post_tit"]/a[@target="_blank"]/@href').extract_first()
			articleItem['sourceUrl'] = BlockobSpider.start_urls[0] + i_item.xpath(
				'.//div[@class="post_meta"]/a[@class="post_author"]/@href').extract_first()
			artTime = \
				i_item.xpath('.//div[@class="post_meta"]/span[@class="post_date"]/text()').extract()[0].split()[1]
			if artTime.__contains__(self.timeReg):
				th=artTime.split(self.timeReg)[0];
				articleItem['artTime']=(datetime.datetime.now()-datetime.timedelta(hours=int(th))).strftime("%Y-%m-%d %H:%M:%S")
			else:
				articleItem['artTime']=artTime
			if articleItem['artTime'] > self.searchEndTime:
				yield articleItem
				if articleItem['artUrl']:
					artUrl = articleItem['artUrl']
					yield scrapy.Request(artUrl, callback=self.parse_detail)
				if artUrl:
					id = re.findall(r'/posts/info/([0-9]+)', artUrl)
				
				else:
					id = False
		if id:
			print("id:", id[0])
			next_link = "https://www.blockob.com/posts/get-recommend-list?id=" + id[0]
			print("next_link", next_link)
			yield scrapy.Request(next_link, callback=self.parse_loadmore_recommend)
	
	# 解析更多的政策文章
	def parse_loadmore_policy(self, response):
		if response.text.__contains__("code"):
			data = json.loads(response.text)
			response = data['data']
		# print(response)
		articleList = Selector(text=response).xpath(
			'//div[@class="post_item clearfix"]')
		# print(articleList)
		for i_item in articleList:
			articleItem = BlockchainprojectItem()
			articleItem['title'] = i_item.xpath('.//h4[@class="post_tit"]/a[@target="_blank"]/text()').extract_first()
			articleItem['introduce'] = i_item.xpath('.//div[@class="post_profile"]/text()').extract_first()
			articleItem['artUrl'] = BlockobSpider.start_urls[0] + i_item.xpath(
				'.//h4[@class="post_tit"]/a[@target="_blank"]/@href').extract_first()
			articleItem['sourceUrl'] = BlockobSpider.start_urls[0] + i_item.xpath(
				'.//div[@class="post_meta"]/a[@class="post_author"]/@href').extract_first()
			artTime = \
				i_item.xpath('.//div[@class="post_meta"]/span[@class="post_date"]/text()').extract()[0].split()[1]
			
			if artTime.__contains__(self.timeReg):
				th = artTime.split(self.timeReg)[0];
				articleItem['artTime'] = (datetime.datetime.now() - datetime.timedelta(hours=int(th))).strftime(
					"%Y-%m-%d %H:%M:%S")
			else:
				articleItem['artTime']=artTime
			if articleItem['artTime'] > self.searchEndTime:
				yield articleItem
				
				if articleItem['artUrl']:
					artUrl = articleItem['artUrl']
					yield scrapy.Request(artUrl, callback=self.parse_detail)
				if artUrl:
					id = re.findall(r'/posts/info/([0-9]+)', artUrl)
				
				else:
					id = False
		if id:
			print("id:", id[0])
			polNext_link = "https://www.blockob.com/posts/get-list-by-term-id?term_id=4&id=" + id[0]
			print("next_link", polNext_link)
			yield scrapy.Request(polNext_link, callback=self.parse_loadmore_policy)
	
	#解析文章内容
	def parse_detail(self, response):
		artBodyItem = ArticleBodyItem()
		artBodyItem['title'] = response.xpath('//div[@class="post_hd"]/h3[@class="post_tit"]/text()').extract()
		artBodyItem['introduce'] = response.xpath(
			'//div[@class="post_hd"]/div[@class="post_generalize"]/text()').extract()
		artBody = response.xpath('//div[@class="post_cont"]//text()').extract()
		print(artBody)
		artString='';
		for item in artBody:
			artString+=item;
		artBodyItem['body'] = artString
		
		# artBodyItem['body'] = ''.join(artContent)
		yield artBodyItem
		artImgItem = ArticleImageItem()
		
		img_urlList = response.xpath('//div[@class="post_cont"]//img/@src').extract()
		
		artImgItem['title'] = artBodyItem['title']
		tag = 1
		dic = {}
		for i in img_urlList:
			dicimg = {}
			dicimg['img_url'] = i
			content = requests.get(i).content
			dicimg['img'] = binary.Binary(content)
			dic[str(tag)] = dicimg
			tag += 1
		artImgItem['img'] = dic
		yield artImgItem
# print(artBodyItem)
