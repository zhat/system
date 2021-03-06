import os
import xlrd
from celery import shared_task
from .models import StatisticsData,ReportData,StatisticsOfPlatform,ProductStock,AmazonOrderItem,ProductInfo
from datetime import datetime,timedelta
from .get_data import get_data,GetStatisticsDataFromOMS
from .read_email import get_email_excel
from django.conf import settings

def clean_data(date):
    """
    """
    asin_info_list = StatisticsData.objects.values('asin','sku','platform','station').filter(date=date).all().distinct()
    currencycode = ""
    for asin_info in asin_info_list:
        if asin_info['asin']=="None":
            continue
        sku = asin_info['sku']
        asin = asin_info['asin']
        platform = asin_info['platform']
        station = asin_info['station']
        sd_list = StatisticsData.objects.filter(date=date,platform=platform,station=station).filter(asin=asin).all()
        qty= 0
        deduction= 0.0
        price = 0.0
        count = 0
        report_data = ReportData.objects.filter(date=date).filter(asin=asin).\
            filter(platform=platform).filter(station=station).first()
        if report_data:
            continue
        for sd in sd_list:
            if currencycode == "" and sd.currencycode != "None":
                currencycode=sd.currencycode
            qty+=sd.qty
            deduction+=round(float(sd.deduction),2)
            price+=round(float(sd.price),2)
            count+=sd.count
        ReportData.objects.create(date=date,sku=sku,asin=asin,platform=platform,station=station,qty=qty,currencycode=currencycode,
                                  deduction=deduction,price=price,count=count)

def del_data(days=0):
    now = datetime.now()
    date = now - timedelta(days=days)
    date = date.strftime("%Y-%m-%d")
    StatisticsOfPlatform.objects.filter(date__gt=date).delete()
    StatisticsData.objects.filter(date__gt=date).delete()
    ReportData.objects.filter(date__gt=date).delete()

@shared_task
def clean():
    """
    清洗前天的数据，放入ReportData表中
    :return:
    """
    #删除最近15天的数据
    del_data(15)
    now = datetime.now()
    days = 30
    gs = GetStatisticsDataFromOMS()
    gs.login()
    zone_info = [
        ('US', 'US', 'Amazon.com'),
        ('UK', 'DE', 'Amazon.co.uk'),
        ('DE', 'DE', 'Amazon.de'),
        ('JP', 'JP', 'Amazon.co.jp'),
        ('CA', 'CA', 'Amazon.ca'),
        ('ES', 'DE', 'Amazon.es'),
        ('IT', 'DE', 'Amazon.it'),
        ('FR', 'DE', 'Amazon.fr'),
    ]
    while days > 1:
        date = now - timedelta(days=days)
        date = date.strftime("%Y-%m-%d")
        has_date = False
        for zone, platform, station in zone_info:
            sp_list = StatisticsOfPlatform.objects.filter(date=date,platform=zone,station=station).all()
            if sp_list:
                continue
            has_date = True
            print(date,zone,platform,station)
            gs.get_data(date=date,zone=zone,platform=platform,station=station)
        if has_date:
            clean_data(date)
            get_route(date)
            get_sum_route(date)
        days -= 1
    return True

@shared_task
def data():
    now = datetime.now()
    days = 2
    date = now - timedelta(days=days)
    date = date.strftime("%Y-%m-%d")
    sp_list = StatisticsOfPlatform.objects.filter(date=date)
    if sp_list:
        return False
    get_data(date)
    clean_data(date)
    get_route(date)
    get_sum_route(date)
    return True

def get_route(date):
    """
    计算单品同比和周环比
    """
    #sametermrate
    #weekrate
    rd_list = ReportData.objects.filter(date=date)
    for rd in rd_list:
        yesteerday = rd.date-timedelta(days=1)
        seven_days_ago = rd.date-timedelta(days=7)
        yesteerday_rd = ReportData.objects.filter(date=yesteerday).filter(asin=rd.asin).\
            filter(platform=rd.platform).filter(station=rd.station)
        if yesteerday_rd and yesteerday_rd[0].price:
            rd.sametermrate = round((rd.price-yesteerday_rd[0].price)/yesteerday_rd[0].price,4)
        else:
            rd.sametermrate=1
        seven_days_ago_rd = ReportData.objects.filter(date=seven_days_ago).filter(asin=rd.asin).\
            filter(platform=rd.platform).filter(station=rd.station)
        if seven_days_ago_rd and seven_days_ago_rd[0].price:
            rd.weekrate=round((rd.price-seven_days_ago_rd[0].price)/seven_days_ago_rd[0].price,4)
        else:
            rd.weekrate=1
        rd.save()

def get_sum_route(date):
    """
    计算站点的周比和同比
    dollar_price
    sametermrate
    weekrate
    :return:
    """
    sp_list = StatisticsOfPlatform.objects.filter(date=date)
    for sp in sp_list:
        yesteerday = sp.date - timedelta(days=1)
        seven_days_ago = sp.date - timedelta(days=7)
        yesteerday_sp = StatisticsOfPlatform.objects.filter(date=yesteerday).\
            filter(platform=sp.platform).filter(station=sp.station)
        if yesteerday_sp and yesteerday_sp[0].dollar_price:
            sp.sametermrate = round((sp.dollar_price-yesteerday_sp[0].dollar_price)/yesteerday_sp[0].dollar_price,4)
        else:
            sp.sametermrate = 0
        seven_days_ago_sp = StatisticsOfPlatform.objects.filter(date=seven_days_ago).\
            filter(platform=sp.platform).filter(station=sp.station)
        if seven_days_ago_sp and seven_days_ago_sp[0].dollar_price:
            sp.weekrate = round((sp.dollar_price-seven_days_ago_sp[0].dollar_price)/seven_days_ago_sp[0].dollar_price,4)
        else:
            sp.weekrate=0

        sp.save()

def get_route2():
    """
    计算单品同比和周环比
    """
    #sametermrate
    #weekrate
    rd_list = ReportData.objects.all()
    for rd in rd_list:
        yesteerday = rd.date-timedelta(days=1)
        seven_days_ago = rd.date-timedelta(days=7)
        yesteerday_rd = ReportData.objects.filter(date=yesteerday).filter(asin=rd.asin)
        if yesteerday_rd and yesteerday_rd[0].price:
            rd.sametermrate = round((rd.price-yesteerday_rd[0].price)/yesteerday_rd[0].price,4)
        else:
            rd.sametermrate=1
        seven_days_ago_rd = ReportData.objects.filter(date=seven_days_ago).filter(asin=rd.asin)
        if seven_days_ago_rd and seven_days_ago_rd[0].price:
            rd.weekrate=round((rd.price-seven_days_ago_rd[0].price)/seven_days_ago_rd[0].price,4)
        else:
            rd.weekrate=1
        rd.save()

def get_sum_route2():
    """
    计算站点的周比和同比
    dollar_price
    sametermrate
    weekrate
    :return:
    """
    sp_list = StatisticsOfPlatform.objects.all()
    for sp in sp_list:
        yesteerday = sp.date - timedelta(days=1)
        seven_days_ago = sp.date - timedelta(days=7)
        yesteerday_sp = StatisticsOfPlatform.objects.filter(date=yesteerday)
        if yesteerday_sp and yesteerday_sp[0].dollar_price:
            sp.sametermrate = round((sp.dollar_price-yesteerday_sp[0].dollar_price)/yesteerday_sp[0].dollar_price,4)
        else:
            sp.sametermrate = 0
        seven_days_ago_sp = StatisticsOfPlatform.objects.filter(date=seven_days_ago)
        if seven_days_ago_sp and seven_days_ago_sp[0].dollar_price:
            sp.weekrate = round((sp.dollar_price-seven_days_ago_sp[0].dollar_price)/seven_days_ago_sp[0].dollar_price,4)
        else:
            sp.weekrate=0

        sp.save()


@shared_task
def get_stock():
    ##从excel文件获取库存
    get_email_excel()
    now = datetime.now()
    i = 30
    while i>=0:
        date = now - timedelta(days=i)
        i-=1
        now_str = date.strftime("%Y%m%d")
        print(now_str)
        file_name = "库存管理总表{}.xlsx".format(now_str)
        base_path = settings.IMAGE_PATH
        file_path = os.path.join(base_path,file_name)
        print(file_path)
        if not os.path.exists(file_path):
            continue
        date_str = date.strftime("%Y-%m-%d")
        if ProductStock.objects.filter(date=date_str):
            continue
        print(date_str)
        data = xlrd.open_workbook(file_path)
        table = data.sheets()[0]
        platform = "US"
        station = "www.amazon.com"
        sku_list = [cell.value if isinstance(cell.value,str) else str(int(cell.value)) for cell in table.col(0)]
        quantity_list = [int(cell.value) if isinstance(cell.value,float) else cell.value for cell in table.col(5)]
        reserved_list = [int(cell.value) if isinstance(cell.value, float) else cell.value for cell in table.col(6)]
        for sku,quantity,reserved in zip(sku_list[2:],quantity_list[2:],reserved_list[2:]):
            stock = quantity+reserved
            ProductStock.objects.create(date=date_str,sku=sku,stock=stock,quantity=quantity,reserved=reserved,
                                        platform=platform,station=station)

@shared_task
def get_product_info_from_order():
    # 从订单表里面获取最近一个月有销量的商品信息
    date = datetime.now()
    last_month = date - timedelta(days=30)
    last_month_str = last_month.strftime("%Y-%m-%d")
    print(datetime.now())
    order_items = AmazonOrderItem.objects.using('remote').values('asin','sku','parent__platform').distinct().\
        filter(parent__purchase_at__gt=last_month_str).order_by('parent__platform').all()
    #print(order_items)
    #print(len(order_items))
    date_str = date.strftime("%Y-%m-%d")
    for order_item in order_items:
        zone = order_item['parent__platform']
        if zone == "GB":
            zone = "UK"
        product_info = ProductInfo.objects.filter(date=date_str,zone=zone,
                                                  asin=order_item['asin']).first()
        if product_info or not order_item['sku']:
            continue
        ProductInfo.objects.create(date=date_str,zone=zone,
                                   asin=order_item['asin'],sku=order_item['sku']).save()

    order_items = ReportData.objects.values('asin', 'sku', 'platform').filter(date__gt=last_month_str).all().distinct()
    # print(order_items)
    # print(len(order_items))
    print(order_items)
    print(len(order_items))
    date_str = date.strftime("%Y-%m-%d")
    for order_item in order_items:
        zone = order_item['platform']
        if zone == "GB":
            zone = "UK"
        product_info = ProductInfo.objects.filter(date=date_str, zone=zone,
                                                  asin=order_item['asin']).first()
        if product_info or not order_item['sku']:
            continue
        ProductInfo.objects.create(date=date_str, zone=zone,
                                   asin=order_item['asin'], sku=order_item['sku']).save()
    print(datetime.now())