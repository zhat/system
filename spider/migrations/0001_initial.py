# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-08 02:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='权限名称')),
                ('url', models.CharField(max_length=255, verbose_name='URL名称')),
                ('per_method', models.SmallIntegerField(choices=[(1, 'GET'), (2, 'POST')], default=1, verbose_name='请求方法')),
                ('argument_list', models.CharField(blank=True, help_text='多个参数之间用英文半角逗号隔开', max_length=255, null=True, verbose_name='参数列表')),
                ('describe', models.CharField(max_length=255, verbose_name='描述')),
            ],
            options={
                'verbose_name_plural': '权限表',
                'verbose_name': '权限表',
                'permissions': (('views_student_list', '查看学员信息表'), ('views_student_info', '查看学员详细信息')),
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='姓名')),
                ('age', models.SmallIntegerField(verbose_name='年龄')),
                ('sex', models.SmallIntegerField(choices=[(1, '男'), (2, '女'), (3, '未知')], verbose_name='性别')),
            ],
        ),
    ]
