# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-29 15:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pyconguide', '0005_remove_calendar_last_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presentation',
            name='speakers',
            field=models.TextField(blank=True, verbose_name='Speakers'),
        ),
    ]