# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-29 15:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pyconguide', '0004_remove_calendar_icalendar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calendar',
            name='last_updated',
        ),
    ]
