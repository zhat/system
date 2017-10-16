# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-11 12:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='日期')),
                ('store', models.CharField(max_length=64, null=True, verbose_name='店铺')),
                ('last_30_days', models.IntegerField(null=True, verbose_name='最近30天')),
                ('last_90_days', models.IntegerField(null=True, verbose_name='最近90天')),
                ('last_12_months', models.IntegerField(null=True, verbose_name='最近12个月')),
                ('lifetime', models.IntegerField(null=True, verbose_name='全部')),
                ('last_day', models.IntegerField(null=True, verbose_name='最近1天')),
                ('last_week', models.IntegerField(null=True, verbose_name='最近1周')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Feedback',
                'verbose_name': 'Feedback',
            },
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(max_length=32, null=True, verbose_name='账号')),
                ('station', models.CharField(max_length=64, null=True, verbose_name='站点')),
            ],
        ),
        migrations.AddField(
            model_name='feedback',
            name='station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.Station'),
        ),
    ]
