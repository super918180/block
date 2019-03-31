# -*- coding: utf-8 -*-
import scrapy
from items import BlockchainprojectItem, ArticleBodyItem, ArticleImageItem
import requests
from bson import binary
import json


class A8btcSpider(scrapy.Spider):
	name = 'a8btc'
	allowed_domains = ['8btc.com']
	orgUrl = 'https://www.8btc.com'
	start_urls = ['https://www.8btc.com/news']
	loadmoreTag = 3
	
	def parse(self, response):
		# 特色文章
		featureBannerArticleItem = BlockchainprojectItem()
		featureBannerArticlePath = response.xpath(
			'//div[@class="main__feature bbt-clearfix"]/div[@class="feature__banner"]/div[@class="feature__banner__title"]')
		featureBannerArticleItem['title'] = featureBannerArticlePath.xpath('.//a/text()').extract()[0].strip()
		featureBannerArticleItem['artUrl'] = self.orgUrl + featureBannerArticlePath.xpath('.//a/@href').extract()[0]
		featureBannerArticleItem['sourceUrl'] = self.start_urls
		yield featureBannerArticleItem
		yield scrapy.Request(featureBannerArticleItem['artUrl'], callback=self.parse_detail)
		# 其他特色文章
		featureThumbArticleList = response.xpath(
			'//div[@class="main__feature bbt-clearfix"]/div[@class="feature__thumb"]')
		for featureThumbArticle in featureThumbArticleList:
			featureThumbArticleItem = BlockchainprojectItem()
			featureThumbArticleItem['title'] = featureThumbArticle.xpath(
				'.//div[@class="feature__thumb__title"]/a/text()').extract()[0].strip()
			featureThumbArticleItem['artUrl'] = self.orgUrl + featureThumbArticle.xpath(
				'.//div[@class="feature__thumb__title"]/a/@href').extract()[0]
			featureThumbArticleItem['sourceUrl'] = self.start_urls
			yield featureThumbArticleItem
		# 其他推荐文章
		remArticleList = response.xpath(
			'//div[@class="bbt-col-xs-17"]//div[@id="news"]//div[@class="article-item-warp"]//div[@class="article-item__body"]')
		for remArticle in remArticleList:
			remArticleItem = BlockchainprojectItem()
			remArticleItem['title'] = remArticle.xpath('./h3[@class="article-item__title"]/a/text()').extract()[
				0].strip()
			remArticleItem['introduce'] = remArticle.xpath('.//div[@class="article-item__content"]/text()').extract()
			remArticleItem['artUrl'] = self.orgUrl + remArticle.xpath(
				'./h3[@class="article-item__title"]/a/@href').extract()[0]
			remArticleItem['sourceUrl'] = remArticle.xpath(
				'.//div[@class="article-item__info bbt-clearfix"]//a[@class="link-dark-major"]/text()').extract()
			yield remArticleItem
			yield scrapy.Request(remArticleItem['artUrl'], callback=self.parse_detail)
		loadmoreStr = response.xpath(
			'//div[@class="bbt-col-xs-17"]//div[@id="news"]//a[@class="bbt-btn bbt-btn--default bbt-btn--lg bbt-btn-block"]/span/text()').extract()[
			0]
		print("loadmoreStr:", loadmoreStr)
		if loadmoreStr == "查看更多":
			url_loadmore = 'https://webapi.8btc.com/bbt_api/news/list?num=20&page=2'
			yield scrapy.Request(url_loadmore, callback=self.parse_loadmore)
	
	def parse_loadmore(self, response):
		data = json.loads(response.text)['data']
		artList = data['list']
		if artList != []:
			for i in artList:
				remArticleItem = BlockchainprojectItem()
				remArticleItem['title'] = i['title']
				remArticleItem['introduce'] = i['desc']
				remArticleItem['artUrl'] = "https://www.8btc.com/article/" + str(i['id'])
				remArticleItem['sourceUrl'] = i['source']['link']
				remArticleItem['artTime'] = i['post_date_format']
				yield remArticleItem
				yield scrapy.Request(remArticleItem['artUrl'], callback=self.parse_detail)
			
			url_loadmore = 'https://webapi.8btc.com/bbt_api/news/list?num=20&page=' + str(self.loadmoreTag)
			yield scrapy.Request(url_loadmore, callback=self.parse_loadmore)
			print(url_loadmore)
			self.loadmoreTag += 1
	
	def parse_detail(self, response):
		
		artBodyItem = ArticleBodyItem()
		artBodyItem['title'] = response.xpath(
			'//div[@class="header__main"]//div[@class="bbt-container"]//h1/text()').extract()
		artBodyItem['body'] = response.xpath(
			'//div[@class="main__body main__body--normal"]//div[@class="bbt-html"]').extract()
		# artBodyItem['body'] = ''.join(artContent).replace('\n', '').replace('\t', '').replace(' ', '')
		yield artBodyItem
		
		img_urlList = response.xpath(
			'//div[@class="main__body main__body--normal"]//div[@class="bbt-html"]//img/@src').extract()
		artImgItem = ArticleImageItem()
		artImgItem['title'] = artBodyItem['title']
		tag = 1
		dic = {}
		for i in img_urlList:
			dicimg = {}
			content = requests.get(i).content
			dicimg['img_url'] = i
			dicimg['img'] = binary.Binary(content)
			tag += 1
			dic[str(tag)] = dicimg
		artImgItem['img'] = dic
		yield artImgItem
