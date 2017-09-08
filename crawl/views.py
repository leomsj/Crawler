# -*- coding: utf-8 -*-
from django.shortcuts import render

# module crawler
import CRAWLER
import FCRAWLER
import NCRAWLER

# module utility
import READ
import URI
import SAVE

# Create your views here.
def crawl(request):
  
  '''
  # 파일 읽기
  fils = READ.Read('df33.csv')
  readFile = fils.reading()
  uris = URI.Uri(readFile,'name').get()
  
  # 크롤링
  
  crawler = CRAWLER.Crawler(
    # 'http://www.cine21.com/search/?q=', 
    'http://movie.naver.com/movie/search/result.nhn?query=',
    uris,
    True
  )
  data = crawler.crawling(
    # cine
    # '.mov_list > li:nth-of-type(1)',
    # {'key': 'title', 'class': '.name > a'},
    # {'key': 'director', 'class': 'p:nth-of-type(3) > a:nth-of-type(1)'},
    # {'key': 'actors', 'class': 'p:nth-of-type(3) span:nth-of-type(2) ~ a'},
    # {'key': 'expert-rating', 'class': 'div:nth-of-type(1) > div:nth-of-type(1) > .num'},
    # {'key': 'user-rating', 'class': 'div:nth-of-type(1) > div:nth-of-type(2) > .num'},
    # naver
    '#old_content > ul:nth-of-type(2) > li:nth-of-type(1)',
    {'key': 'title', 'class': 'dt:nth-of-type(1) > a'},
    {'key': 'director', 'class': 'dd:nth-of-type(3) > a:nth-of-type(1)'},
    {'key': 'actors', 'class': 'dd:nth-of-type(3) a:nth-of-type(2) ~ a'},
    {'key': 'user-rating', 'class': 'dd:nth-of-type(1) > .num'},
  )

  # 파일 저장
  save = SAVE.Save(data, 'naver-df33')
  save.json()
  save.csv()
  # save.db()
  '''
  
  '''
  datas = FCRAWLER.FCrawler("1994452547456105", "c9eb03a95fabab570ee4d5734543eebf", "119682344771692", "2017-08-15", "2017-08-30").crawling()
  save1 = SAVE.Save(datas, 'facebook-cgv-2016-08-30-2017-08-30')
  '''

  '''
  ncrawler = NCRAWLER.NCrawler('_Bojjkpb60ufmH4_kana', 'D6ZyhdC2fx').crawling()
  '''

  return render(request, 'crawl/index.html', { 'req' : 1})