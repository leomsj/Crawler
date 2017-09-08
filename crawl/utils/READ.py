# -*- coding: utf-8 -*-
import os

# data format
import json
import csv

class Read:

  # constructer
  def __init__(self, fileName, filePath='data/material'):
    self.fileName = fileName
    self.filePath = filePath
  
  # leading 함수
  def reading(self, *categorize):
    # 변수 선언
    readData = list()
    fileFormat = os.path.splitext(self.fileName)[1]
    
    # 패스 설정
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # 파일 디렉토리
    UPPATH = lambda _path, n: os.sep.join(_path.split(os.sep)[:-n]) # 상위 디렉토리 이동

    # 파일 확장자가 csv인 경우
    if fileFormat == '.csv':
      with open(os.path.join(UPPATH(BASE_DIR, 2), self.filePath, self.fileName)) as csvFile:
        read = csv.DictReader(csvFile)
        # 한 열씩 순회
        for row in read:
          data = {} # 빈 객체 생성
          # categorize가 있을 경우 카테고리에 따라 분류
          if categorize:
            # cateogorize 배열 순회
            for i in range(len(categorize)):
              try:
                data[categorize[i]] = row[categorize[i]]
              except:
                print('no category')
          
          # categorize가 없을 경우
          else:
            for key, value in row.items():
              data[key] = row[key]
          
          # data를 readData에 추가
          readData.append(data)
    
    # 파일 확장자가 json인 경우
    elif fileFormat == '.json':
      with open(os.path.join(UPPATH(BASE_DIR, 2), self.filePath, self.fileName)) as jsonFile:
        read = json.load(jsonFile)
        # 한 객체씩 순회
        for item in read:
          data = {} # 빈 객체 생성
          # categorize가 있을 경우 카테고리에 따라 분류
          if categorize:
            for category in categorize:
              try:
                data[category] = item[category]
              except:
                print('no category')
          # categorize가 없을 경우
          else:
            data = item

          # data를 readData에 추가
          readData.append(data)

    # csv 혹은 json이 아닌 경우
    else:
      print('reading fail')

    return readData