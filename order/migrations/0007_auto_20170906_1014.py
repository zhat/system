# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-06 10:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_amazonorder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='amazonorder',
            name='update_time',
        ),
        migrations.AddField(
            model_name='amazonorder',
            name='amazon_order_id',
            field=models.IntegerField(blank=True, editable=False, null=True, verbose_name='ID'),
        ),
    ]
