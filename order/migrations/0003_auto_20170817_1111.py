# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-17 11:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20170815_1432'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderdata',
            name='order_table_id',
        ),
        migrations.AddField(
            model_name='orderdata',
            name='status',
            field=models.CharField(blank=True, editable=False, max_length=50, null=True, verbose_name='订单状态'),
        ),
    ]
