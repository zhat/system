# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-22 17:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0002_auto_20170914_1805'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmazonProductBaseinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zone', models.CharField(blank=True, max_length=8, null=True)),
                ('asin', models.CharField(blank=True, max_length=20, null=True)),
                ('ref_id', models.CharField(blank=True, max_length=20, null=True)),
                ('seller_name', models.CharField(blank=True, max_length=50, null=True)),
                ('seller_url', models.CharField(blank=True, max_length=100, null=True)),
                ('brand', models.CharField(blank=True, max_length=50, null=True)),
                ('brand_url', models.CharField(blank=True, max_length=100, null=True)),
                ('is_fba', models.CharField(blank=True, max_length=2, null=True)),
                ('stock_situation', models.CharField(blank=True, max_length=50, null=True)),
                ('category_name', models.CharField(blank=True, max_length=255, null=True)),
                ('original_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('in_sale_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('review_cnt', models.IntegerField(blank=True, null=True)),
                ('review_avg_star', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('percent_5_star', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('percent_4_star', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('percent_3_star', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('percent_2_star', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('percent_1_star', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('cnt_qa', models.IntegerField(blank=True, null=True)),
                ('offers_url', models.CharField(blank=True, max_length=200, null=True)),
                ('lowest_price', models.DecimalField(blank=True, decimal_places=2, max_digits=11, null=True)),
                ('create_date', models.DateTimeField()),
                ('update_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'amazon_product_baseinfo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProductStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='日期')),
                ('sku', models.CharField(max_length=128, null=True, verbose_name='sku')),
                ('asin', models.CharField(max_length=128, null=True, verbose_name='asin')),
                ('platform', models.CharField(max_length=32, null=True, verbose_name='账号')),
                ('station', models.CharField(max_length=64, null=True, verbose_name='站点')),
                ('stock', models.IntegerField(null=True, verbose_name='库存数')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '库存信息表',
                'verbose_name': '库存信息表',
            },
        ),
    ]