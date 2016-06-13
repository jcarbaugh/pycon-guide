# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-29 15:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pyconguide', '0002_calendar'),
    ]

    operations = [
        migrations.AddField(
            model_name='presentation',
            name='room',
            field=models.CharField(blank=True, max_length=64, verbose_name='Room'),
        ),
        migrations.AddField(
            model_name='presentation',
            name='speakers',
            field=models.CharField(blank=True, max_length=255, verbose_name='Speakers'),
        ),
    ]
