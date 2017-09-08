# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone

# Create your models here.
class CrawlData(models.Model):
  no = models.AutoField(primary_key=True)
  date = models.DateTimeField(default=timezone.now)
  title = models.CharField(max_length=200) # 글자 수 200자 이내인 title
  director = models.CharField(null=True, max_length=50)
  expert_rating = models.FloatField(null=True)
  user_rating = models.FloatField(null=True)
  # link = models.URLField()

  def __str__(self):
    return self.title