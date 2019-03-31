# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BlockchainprojectItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	type=scrapy.Field()
	title = scrapy.Field()
	introduce = scrapy.Field()
	artUrl = scrapy.Field()
	sourceUrl = scrapy.Field()
	artTime = scrapy.Field()


class ArticleBodyItem(scrapy.Item):
	title = scrapy.Field()
	introduce = scrapy.Field()
	body = scrapy.Field()


class ArticleImageItem(scrapy.Item):
	title = scrapy.Field()
	artUrl = scrapy.Field()
	img = scrapy.Field()
