# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-06-11 06:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0014_rawleads_whois'),
    ]

    operations = [
        migrations.CreateModel(
            name='ZoneFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zone_type', models.CharField(max_length=10)),
                ('zone_name', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'zone_files',
            },
        ),
        migrations.DeleteModel(
            name='ZoneDomains',
        ),
    ]
