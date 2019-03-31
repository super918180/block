from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request
from lxml import etree
import time


class getProxyIP():
	def __init__(self):
		self.url = "https://www.kuaidaili.com/free/"
		self.ipList = []
	
	# 获取IP地址
	def getIP(self, pageNum):
		self.ipList.append(self.parseHtml(self.url))
		for i in range(pageNum):
			nextUrl = self.url + 'inha/' + str(i + 1)
			self.ipList.append(self.parseHtml(nextUrl))
		return self.ipList
	
	# 解析地址
	def parseHtml(self, strUrl):
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
		}
		request = urllib.request.Request(url=strUrl, headers=headers)
		print(strUrl)
		response = urllib.request.urlopen(request)
		time.sleep(2)
		print(response)
		html = response.read().decode('utf-8')
		content = etree.HTML(html)
		items = content.xpath('//tbody/tr')
		ipDict = {}
		for item in items:
			ip = item[0].text
			port = item[1].text
			ipDict[ip] = port
		return ipDict
	
	# 多线程提取可用的地址
	def startThread(self):
		avaIPList = []
		len(self.ipList)
		with ThreadPoolExecutor(max_workers=3) as executors:
			future_list = []
			for i in self.ipList:
				future = executors.submit(self.availableProxyIP, i)
				future_list.append(future)
			for res in as_completed(future_list):
				avaIPList.append(res.result())
		print(avaIPList)
		return avaIPList
	
	# 获取可用的地址
	def availableProxyIP(self, dict):
		avaProxyDict = {}
		count = 0;
		for (k, v) in dict.items():
			print(k, v)
			proxy = urllib.request.ProxyHandler({"http": "http://" + k + ":" + v})
			opener = urllib.request.build_opener(proxy)
			urllib.request.install_opener(opener)
			time.sleep(2)
			try:
				data = urllib.request.urlopen('http://www.baidu.com', timeout=5).read().decode('utf-8', 'ignore')
				if (len(data) > 5000):
					avaProxyDict[k] = v
					count = count + 1
					print('有效')
				else:
					print(':无效')
			except:
				print(':无效！！!')
		# print('可用数据有' + str(count) + "条")
		return avaProxyDict
	
	# 将地址写入文件中
	def writeTxt(self, path, List):
		print()
		with open(path, 'w+') as f:
			for i in range(len(List)):
				dict = List[i]
				if len(dict) == 0:
					pass;
				else:
					for (k, v) in dict.items():
						f.writelines(k + ":" + v+'\n')
		print("文件写完成")
	
	def readTxt(self, path):
		with open(path, 'r') as f:
			ipList=f.readlines()
			return ipList


if __name__ == '__main__':
	# 想要获取的IP页面数，一个页面15条
	ipPageNum = 10;
	path = 'D:\\test.txt'
	test = getProxyIP()
	dict = test.getIP(ipPageNum)
	# dict = test.availableProxyIP(dict)
	avaIPList = test.startThread()
	test.writeTxt(path, avaIPList);
	#验证文件中的IP列表是否可用
	# ipList=test.readTxt()
	# for i in range(len(ipList)):
	# 	test.availableProxyIP(i)