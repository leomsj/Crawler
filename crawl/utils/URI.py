# -*- coding: utf-8 -*-

class Uri:
  
  # constructer
  def __init__(self, listFile, key):
    self.listFile = listFile
    self.key = key
  
  # getUri 함수
  def get(self):
    # 변수 선언
    uris = list()
    
    # listFile 순회
    for each in self.listFile:
      uris.append(each[self.key])

    return uris
