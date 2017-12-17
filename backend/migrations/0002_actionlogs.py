# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-14 19:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionLogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_thats_changed', models.CharField(max_length=25)),
                ('old_value', models.CharField(max_length=100)),
                ('new_value', models.CharField(max_length=100)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Lead')),
            ],
            options={
                'db_table': 'action_logs',
            },
        ),
    ]