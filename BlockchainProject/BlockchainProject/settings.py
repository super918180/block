# -*- coding: utf-8 -*-

# Scrapy settings for BlockchainProject project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'BlockchainProject'

SPIDER_MODULES = ['BlockchainProject.spiders']
NEWSPIDER_MODULE = 'BlockchainProject.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:

# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# 默认Item并发数：100
CONCURRENT_ITEMS = 100
# 默认 Request 并发数：16
CONCURRENT_REQUESTS = 16
# 默认每个域名的并发数：8
CONCURRENT_REQUESTS_PER_DOMAIN = 8
# 每个IP的最大并发数：0表示忽略
CONCURRENT_REQUESTS_PER_IP = 0

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'BlockchainProject.middlewares.BlockchainprojectSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
	# 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware':110,
	# 'BlockchainProject.middlewares.IPPOOlS': 125,
	'BlockchainProject.middlewares.BlockchainprojectDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
	'BlockchainProject.pipelines.BlockchainprojectPipeline': 10,
	# 'BlockchainProject.pipelines.OdailyPipeline': 50,
	# 'BlockchainProject.pipelines.A8btcPipeline': 100,
	
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 设置IP池
# IPPOOL = [
# {"ipaddr": "112.98.126.100:33421"},
# 	# {"ipaddr": "61.152.81.193:9100"},{"ipaddr": "120.204.85.29:3128"},{"ipaddr": "219.228.126.86:8123"},
# 	# {"ipaddr": "61.152.81.193:9100"},
# 	# {"ipaddr": "218.82.33.225:53853"},
# 	# {"ipaddr": "223.167.190.17:42789"}
# ]

COMMANDS_MODULE = 'BlockchainProject.commands'
IPPOOLPath = 'D:\\test.txt'

HTTPERROR_ALLOWED_CODES = [403,404]

mongodb_host = '127.0.0.1'
mongodb_port = 27017
mongodb_db = 'blockchain'
mongodb_coll_article_catalog = 'article_catalogs'
mongodb_coll_article_body = 'article_bodys'
mongodb_coll_article_img = 'article_imgs'
