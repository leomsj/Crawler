# -*- coding: utf-8 -*-
import os
import re
import time
import urllib.parse

# module import for crawling
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

class Crawler:

  # constructer
  def __init__(self, host, uris, daynamic=False, button={}):
    self.host = host
    self.uris = uris
    self.daynamic = daynamic
    self.button = button
    self.crawlingData = list() # 크롤링 데이터를 담을 list type의 변수 할당

  # 크롤링 함수
  def crawling(self, selecter, *selecters):
    # uris가 배열인 경우
    if isinstance(self.uris, list):
      # uris 배열 순회
      for uri in self.uris:
        # 크롤링 할 사이트가 동적으로 데이터를 랜더링 할 경우
        if self.daynamic:
          self.dataDriver(uri, selecter, selecters=selecters)

        # 크롤링 할 사이트가 정적으로 데이터를 랜더링 할 경우 (ex:server side rendering)
        else:
          self.dataRequest(uri, selecter, selecters=selecters)

    # uris가 배열이 아닌 경우
    else:
      # 동적 데이터 크롤링을 위한 chrome 실행 (ex:client side rendering)
      if self.daynamic:
        self.dataDriver(self.uris, selecter, selecters=selecters)

      # 크롤링 할 사이트가 정적으로 데이터를 랜더링 할 경우 (ex:server side rendering)
      else:
        self.dataRequest(self.uris, selecter, selecters=selecters)

    return self.crawlingData
  
  # request 요청 
  def dataRequest(self, uri, selecter, selecters):
    # url(host+uri) 요청
    request = requests.get(self.host + urllib.parse.quote(uri) + '=all&ie=utf8')
    requestSuccess = 0
    while requestSuccess < 5:
      requestSuccess += 1
      print(requestSuccess)
      # 요청 성공시
      if request.status_code == 200:
        print('request success') # 성공 메세지 출력
        requestText = request.text # request 텍스트를 변수에 할당
        self.parser(requestText, selecter, selecters) # parser 함수 호출
        break

      # 요청 실패시
      else:
        print('request fail') # 실패 메세지 출력

  
  # driver 요청
  def dataDriver(self, uri, selecter, selecters):
    # 패스 설정
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # 파일 디렉토리
    UPPATH = lambda _path, n: os.sep.join(_path.split(os.sep)[:-n]) # 상위 디렉토리 이동

    # 동적 데이터 크롤링을 위한 chrome 실행 (ex:client side rendering)
    driver = webdriver.Chrome(os.path.join(UPPATH(BASE_DIR, 2), 'driver','chromedriver'))
    driver.implicitly_wait(5) # 대기 시간

    # 요청 시도
    try:
      # driver로 uri 접속
      driver.get(self.host + urllib.parse.quote(uri) + '=all&ie=utf8')
      time.sleep(0.2)
      print(self.host + urllib.parse.quote(uri) + '=all&ie=utf8')

      '''
      # 더보기 클릭 이벤트
      if self.button['is']:
        for i in range(self.button['count']):
          driver.find_element_by_xpath('//*[@%s="%s"]'%(self.button['attr'], self.button['value'])).click()
          time.sleep(0.5) # 클릭 후 대기
      '''

      # 요청 성공시
      print('request success') # 성공 메세지 출력
      requestText = driver.page_source # request 텍스트를 변수에 할당
      self.parser(requestText, selecter, selecters) # parser 함수 호출

      # 브라우저 닫기
      driver.quit()
    
    # 요청 실패시
    except:
      print('request fail') # 실패 메세지 출력

  # parser 로직
  def parser(self, requestText, selecter, selecters):
    # 변수 선언
    pattern = re.compile(r'\s+') # 빈 공백을 제거하기 위한 정규표현식
    
    # BeautifulSoup
    html = BeautifulSoup(requestText, 'html.parser') # Beautiful로 생성된 객체 할당 #from_encoding='utf-8'
    selectHtml = html.select(selecter) # 선택된 객체 할당
      
    # 객체 배열 순회
    for eachSelectHtml in selectHtml:
      data = {} # 빈 객체 생성
      
      # 특정 클래스에 의해 데이터 가공
      if selecters:
        for each in selecters:
          try:
            # 해당 객체가 여러개일 경우 배열로 순회
            if(len(eachSelectHtml.select(each['class'])) > 1):
              val = ''
              for i in range(len(eachSelectHtml.select(each['class']))):
                val += re.sub(pattern, '', eachSelectHtml.select(each['class'])[i].get_text())
                if i < len(eachSelectHtml.select(each['class'])) - 1: # 맨 마지막을 제외하고 ',' 추가
                  val += ','
              print(val) # 객체 텍스트 출력
              data[each['key']] = val
            # 여러개가 아닐 경우 첫 번째 값 할당
            else:
              print(eachSelectHtml.select(each['class'])[0].get_text()) # 객체 텍스트 출력
              data[each['key']] = re.sub(pattern, '', eachSelectHtml.select(each['class'])[0].get_text())
          # 오류가 났을 경우 무시
          except:
            data[each['key']] = ''
            print('%s is no data'%(each['key'])) # 오류 메세지 출력
            pass

      # 특정 가공할 데이터가 없을 경우 html 반환
      else:
        data['html'] = eachSelectHtml
        
      # 데이터를 리스트에 추가
      print(data) # data 출력
      self.crawlingData.append(data)