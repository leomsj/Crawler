# -*- coding: utf-8 -*-
import json
import time
import os
import re
import urllib.parse
import datetime

# module import for crawling
import requests

class FCrawler:

	# constructer
	def __init__(self, appId, appSecret, pageId, since, until):
		self.appId = appId # https://developers.facebook.com
		self.appSecret = appSecret # https://developers.facebook.com
		self.accessToken = appId + "|" + appSecret
		self.pageId = pageId # https://findmyfbid.com/
		self.since = since # 0000-00-00
		self.until = until # 0000-00-00
		self.data = ''
		self.crawlType = ''
		self.crawlingData = list()
	
	# 크롤링 함수
	def crawling(self, crawlType='feed'):
		self.crawlType = crawlType

		if crawlType == 'feed':
			self.getFacebookFeedData(self.pageId, self.accessToken, self.since, self.until)
		elif crawlType == 'video' or crawlType == 'videos':
			self.getFacebookVideoData(self.pageId, self.accessToken, self.since, self.until)
		else:
			return print('error not supported crawling data type')
		
		return self.crawlingData

	# 요청 반복 
	def requestDataInterval(self, datas):
		if datas['data']: # 데이터가 있을 경우
			try:
				for i in range(len(datas['data'])):
					dataObj = {}
					messageId = '' if 'id' not in datas['data'][i].keys() else datas['data'][i]['id']
					message = '' if 'message' not in datas['data'][i].keys() else datas['data'][i]['message']
					createdTime = '' if 'created_time' not in datas['data'][i].keys() else datas['data'][i]['created_time']
					likesCount = 0 if 'likes' not in datas['data'][i].keys() else datas['data'][i]['likes']['summary']['total_count']
					commentData = '' if 'comments' not in datas['data'][i].keys() else datas['data'][i]['comments']['data']
					# vidoe
					description = '' if 'description' not in datas['data'][i].keys() else datas['data'][i]['description']
					source = '' if 'source' not in datas['data'][i].keys() else datas['data'][i]['source']
					
					# comment loop
					if commentData:
						comments = ''
						for data in commentData:
							comments = comments + data['message'] + '\n'
						commentData = comments
					
					# data dict
					dataObj['id'] = messageId
					dataObj['message'] = message
					dataObj['date'] = createdTime
					dataObj['like'] = likesCount
					dataObj['comment'] = commentData

					self.crawlingData.append(dataObj)

					if i == len(datas['data']) - 1:
						if datas['paging']['next']:
							try:
								self.requestUntilSucced(datas['paging']['next'])
							except KeyError:
								print('feed end')
			except:
				pass
		
	
	# facebook 접속해서 feed 데이터 가져오기
	def getFacebookFeedData(self, pageId, accessToken, since, until):
		# construct the URL string
		base = 'https://graph.facebook.com'
		node = '/' + pageId + '/feed'
		parameters1 = '/?fields=message,created_time,likes.limit(1).summary(true),'
		# -b - cf -  comments.fields(message,parent).summary(true) (- cannot see replies) 
		# -b - changed if you add parent in  filter(stream){message,id,'parent'}, you can see parent
		parameters2 = 'comments.summary(true).filter(stream){message}'

		time = '&since=%s&until=%s'%(since, until)
		access = '&access_token=%s'%(accessToken)
		url = base + node + parameters1 + parameters2 + time + access

		self.requestUntilSucced(url)
	
	# facebook 접속해서 video 데이터 가져오기
	def getFacebookVideoData(self, pageId, accessToken, since, until):
		# construct the URL string
		base = 'https://graph.facebook.com'
		node = '/' + pageId + '/video'
		parameters1 = '/?fields=description,created_time,event,from,likes.limit(1).summary(true),source,'
		# -b - cf -  comments.fields(message,parent).summary(true) (- cannot see replies) 
		# -b - changed if you add parent in  filter(stream){message,id,'parent'}, you can see parent
		parameters2 = 'comments.summary(true).filter(stream){message}'
		time = '&since=%s&until=%s'%(since, until)
		access = '&access_token=%s'%(accessToken)
		url = base + node + parameters1 + parameters2 + time + access

		self.requestUntilSucced(url)
	
	# 요청 회수 5까지 facebook 연결 요청 
	def requestUntilSucced(self, url):
		self.data = '' # data 초기화
		request = requests.get(url)
		requestCount = 0
		while requestCount < 5:
			try:
				if request.status_code == 200:
					print('request success') # 성공 메세지 출력
					self.data = request.json() # request 텍스트를 변수에 할당
					break
			except Exception:
				time.sleep(5)
				print ('request fail %s'%(url))
			# 요청 횟수 1 증가
			requestCount += 1
		self.requestDataInterval(self.data)