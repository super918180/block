# -*- coding: utf-8 -*-
import scrapy
from BlockchainProject.items import BlockchainprojectItem, ArticleBodyItem, ArticleImageItem
import json
import requests
from bson import binary


class OdailySpider(scrapy.Spider):
	name = 'odaily'
	allowed_domains = ['www.odaily.com']
	start_urls = ['https://www.odaily.com/api/pp/api/app-front/feed-stream?feed_id=280&b_id=&per_page=15']
	org_url = "https://www.odaily.com/"
	spiderEndTime='2019-03-01'
	mReg = '分钟前'
	hReg = '小时前'
	dReg = '天前'
	
	def parse(self, response):
		data = json.loads(response.text)['data']
		itemList = data['items']
		id = 0
		for remArticle in itemList:
			remArticleItem = BlockchainprojectItem()
			remArticleItem['type']='recommend'
			remArticleItem['title'] = remArticle['title']
			remArticleItem['artUrl'] = 'https://www.odaily.com/post/' + str(remArticle['entity_id'])
			remArticleItem['sourceUrl'] = self.org_url
			remArticleItem['artTime'] = remArticle['published_at']
			id = remArticle['id']
			if 	remArticleItem['artTime']>=self.spiderEndTime:
				yield remArticleItem
				yield scrapy.Request(remArticleItem['artUrl'], callback=self.parse_detail)
		if id != 0:
			next_link = 'https://www.odaily.com/api/pp/api/app-front/feed-stream?feed_id=280&b_id=' + str(
				id) + '&per_page=10'
			yield scrapy.Request(next_link, callback=self.parse)
	
	def parse_detail(self, response):
		artBodyItem = ArticleBodyItem()
		artBodyItem['title'] = response.xpath(
			'//article[@class="_1ZUFh6Su"]/div[@class="_30dHyM_c"]/h4/text()').extract()
		artBodyItem['introduce'] = response.xpath(
			'//article[@class="_1ZUFh6Su"]/div[@class="_30dHyM_c"]/p[@class="_2Du8-rqZ"]/text()').extract()
		artBodyItem['body'] = response.xpath(
			'//article[@class="_1ZUFh6Su"]/div[@class="_30dHyM_c"]/div[@class="_3739r7Mk"]//text()').extract()
		# artBodyItem['body'] = ''.join(artContent).replace('\n', '').replace('\t', '').replace(' ', '')
		yield artBodyItem
		img_urlList = response.xpath(
			'//article[@class="_1ZUFh6Su"]/div[@class="_30dHyM_c"]/div[@class="_3739r7Mk"]//img/@src').extract()
		
		tag = 1
		artImgItem = ArticleImageItem()
		artImgItem['title'] = artBodyItem['title']
		dic = {}
		for i in img_urlList:
			dicimg = {}
			content = requests.get(i).content
			dicimg['img_url'] = i
			dicimg['img'] = binary.Binary(content)
			dic[str(tag)] = dicimg
			tag += 1
		artImgItem['img'] = dic
		yield artImgItem
