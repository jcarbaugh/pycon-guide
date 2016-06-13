# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-25 21:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import pyconguide.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Presentation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('presentation_id', models.PositiveSmallIntegerField(verbose_name='PyCon ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('url', models.URLField(blank=True, verbose_name='URL')),
                ('category', models.CharField(blank=True, max_length=128, verbose_name='Category')),
                ('audience', models.CharField(blank=True, max_length=64, verbose_name='Audience')),
                ('abstract', models.TextField(blank=True, verbose_name='Abstract')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('start_time', models.DateTimeField(verbose_name='Start Time')),
                ('end_time', models.DateTimeField(verbose_name='End Time')),
                ('duration_minutes', models.PositiveSmallIntegerField(blank=True, help_text='Presentation duration in minutes', null=True, verbose_name='Duration')),
            ],
            options={
                'ordering': ('start_time', 'end_time', 'title'),
            },
        ),
        migrations.CreateModel(
            name='PyCon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveSmallIntegerField(default=pyconguide.models.this_year, unique=True, verbose_name='Year')),
                ('location', models.CharField(help_text='The locality and region where the conference is held', max_length=128, verbose_name='Location')),
            ],
            options={
                'verbose_name_plural': 'PyCons',
                'ordering': ('-year',),
                'verbose_name': 'PyCon',
            },
        ),
        migrations.AddField(
            model_name='presentation',
            name='pycon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='presentations', to='pyconguide.PyCon'),
        ),
        migrations.AddField(
            model_name='interest',
            name='presentation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interests', to='pyconguide.Presentation'),
        ),
        migrations.AddField(
            model_name='interest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interests', to=settings.AUTH_USER_MODEL),
        ),
    ]
