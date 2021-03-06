# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-28 13:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CrawlData',
            fields=[
                ('no', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=200)),
                ('director', models.CharField(blank=True, max_length=50)),
                ('expert_rating', models.FloatField(blank=True)),
                ('user_rating', models.FloatField(blank=True)),
            ],
        ),
    ]
