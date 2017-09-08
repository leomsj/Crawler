# 네이버 검색 API예제는 블로그를 비롯 전문자료까지 호출방법이 동일하므로 blog검색만 대표로 예제를 올렸습니다.
# 네이버 검색 Open API 예제 - 블로그 검색
import os
import sys
import urllib.request
import ssl

class NCrawler:

  def __init__(self, id, secret):
    self.id = id
    self.secret = secret
    self.crawlingData = list()
  
  def crawling(self):
    ssl._create_default_https_context = ssl._create_unverified_context
    client_id = self.id
    client_secret = self.secret
    encText = urllib.parse.quote("히말라야")
    url = "https://openapi.naver.com/v1/search/movie?query=" + encText + "&display=100"  # json 결과
    # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        print(response_body.decode('utf-8'))
        self.crawlingData.append(response_body.decode('utf-8'))
        return self.crawlingData
    else:
        print("Error Code:" + rescode)
  