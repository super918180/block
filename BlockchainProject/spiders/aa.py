# -*- coding: utf-8 -*-
import scrapy

import requests
# from bson import binary


class AaSpider(scrapy.Spider):
	name = 'aa'
	allowed_domains = ['www.odaily.com/post/5136472']
	start_urls = ['https://www.odaily.com/post/5136472/']
	
	def parse(self, response):
		title = response.xpath(
			'//article[@class="_1ZUFh6Su"]/div[@class="_30dHyM_c"]/h4/text()').extract()
		img_urlList = response.xpath(
			'//article[@class="_1ZUFh6Su"]/div[@class="_30dHyM_c"]/div[@class="_3739r7Mk"]//img/@src').extract()
		tag = 1
		artImgItem = ArticleImageItem()
		artImgItem['title'] = title
		dic = {}
		for i in img_urlList:
			dicimg = {}
			content = requests.get(i).content
			dicimg['img_url'] = i
			dicimg['img'] = binary.Binary(content)
			# artImgItem['tag'] = tag
			# artImgItem['img_url'] = i
			# artImgItem['img'] = binary.Binary(content)
			dic[str(tag)] = dicimg
			tag += 1
		
		artImgItem['img'] = dic
		yield artImgItem
