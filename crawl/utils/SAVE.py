# -*- coding: utf-8 -*-
import os
from django.db import models
from crawl.models import CrawlData

# data format
import json
import csv

class Save:

  def __init__(self, fileData, fileName, filePath='data/crowling'):
    self.fileData = fileData
    self.fileName = fileName
    self.filePath = filePath
  
  # csv 파일 저장
  def csv(self):
    # 패스 설정
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # 파일 디렉토리
    UPPATH = lambda _path, n: os.sep.join(_path.split(os.sep)[:-n]) # 상위 디렉토리 이동

    with open(os.path.join(UPPATH(BASE_DIR, 2), self.filePath, self.fileName + '.csv'),'wt') as csvFile:
      writer = csv.writer(csvFile)
      title = list(self.fileData[0].keys())

      # 제목 생성
      writer.writerow(title)

      # 컨텐츠 생성
      for eachData in self.fileData:
        contents = list(eachData.values())
        writer.writerow(contents)

    # return
    return print('csv file save success')

  # josn 파일 저장
  def json(self):
    # 패스 설정
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # 파일 디렉토리
    UPPATH = lambda _path, n: os.sep.join(_path.split(os.sep)[:-n]) # 상위 디렉토리 이동
    
    # json 생성
    with open(os.path.join(UPPATH(BASE_DIR, 2), self.filePath, self.fileName + '.json'), 'w+') as jsonFile:
      json.dump(self.fileData, jsonFile, ensure_ascii=False, indent=4)
    
    # return
    return print('json file save success')

  def db(self):
    for eachData in self.fileData: 
      CrawlData.objects.create(title=eachData['title'], director=eachData['director'], expert_rating=eachData['expert-rating'], user_rating=eachData['user-rating'])

    return print('database save success')