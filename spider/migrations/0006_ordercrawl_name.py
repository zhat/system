# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-09 07:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spider', '0005_auto_20170809_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordercrawl',
            name='name',
            field=models.CharField(blank=True, help_text='购买人姓名', max_length=255),
        ),
    ]
