# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-07-06 11:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0015_auto_20170611_0653'),
    ]

    operations = [
        migrations.RenameField(
            model_name='setting',
            old_name='redempion_row',
            new_name='redempion_row_1',
        ),
        migrations.AddField(
            model_name='setting',
            name='redempion_row_2',
            field=models.SmallIntegerField(default=1),
        ),
    ]
