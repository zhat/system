import time
from celery import shared_task
from .models import StatisticsData,ReportData,AsinInfo,StatisticsOfPlatform
from datetime import datetime,timedelta

@shared_task
def add(x, y):
    time.sleep(10)
    return x + y

#@shared_task
def clean_data(date):
    """
    date = models.DateField("日期")
    sku = models.CharField("sku", max_length=128, null=True)
    asin = models.CharField("asin", max_length=128, null=True)
    platform = models.CharField("账号", max_length=32, null=True)
    station = models.CharField("站点", max_length=64, null=True)
    qty = models.IntegerField("订单数量", null=True)
    currencycode = models.CharField("币种", max_length=32, null=True)
    deduction = models.CharField("折扣额", max_length=128, null=True)
    price = models.CharField("金额", max_length=128, null=True)
    count = models.IntegerField("总数", null=True)
    sametermrate = models.CharField("同比", max_length=64, null=True)
    weekrate = models.CharField("周环比", max_length=64, null=True)
    monthrate = models.CharField("月环比", max_length=64, null=True)
    status = models.CharField("订单状态", max_length=32, null=True)
    """
    asin_info_list = AsinInfo.objects.filter(date=date).all()
    currencycode = ""
    for asin_info in asin_info_list:
        if asin_info.asin=="None":
            continue
        sd_list = StatisticsData.objects.filter(date=date).filter(asin=asin_info.asin).all()
        sku=asin_info.sku
        asin=asin_info.asin
        platform = asin_info.platform
        station = asin_info.station
        qty= 0
        deduction= 0.0
        price = 0.0
        count = 0
        for sd in sd_list:
            if currencycode=="" and sd.currencycode!="None":
                currencycode=sd.currencycode
            qty+=sd.qty
            deduction+=round(float(sd.deduction),2)
            price+=round(float(sd.price),2)
            count+=sd.count
        ReportData.objects.create(date=date,sku=sku,asin=asin,platform=platform,station=station,qty=qty,currencycode=currencycode,
                                  deduction=deduction,price=price,count=count)

def clean():
    now = datetime.now()
    days = 2
    while days < 30:
        date = now - timedelta(days=days)
        date = date.strftime("%Y-%m-%d")
        clean_data(date)
        days += 1
        time.sleep(5)


def get_route():
    #sametermrate
    #weekrate
    rd_list = ReportData.objects.all()
    for rd in rd_list:
        yesteerday = rd.date-timedelta(days=1)
        print(yesteerday)
        seven_days_ago = rd.date-timedelta(days=7)
        print(seven_days_ago)
        yesteerday_rd = ReportData.objects.filter(date=yesteerday).filter(asin=rd.asin)
        print(yesteerday_rd)
        if yesteerday_rd and yesteerday_rd[0].price:
            print(rd.price)
            print(yesteerday_rd[0].price)
            rd.sametermrate = round(rd.price/yesteerday_rd[0].price,4)
            print(rd.sametermrate)
        else:
            rd.sametermrate=0
        seven_days_ago_rd = ReportData.objects.filter(date=seven_days_ago).filter(asin=rd.asin)
        if seven_days_ago_rd and seven_days_ago_rd[0].price:
            print(rd.price)
            print(seven_days_ago_rd[0].price)
            print((rd.price)/(seven_days_ago_rd[0].price))
            rd.weekrate=round(rd.price/seven_days_ago_rd[0].price,4)
            print(rd.weekrate)
        else:
            rd.weekrate=0
        rd.save()

def get_sum_route():
    """
    dollar_price
    sametermrate
    weekrate
    :return:
    """
    sp_list = StatisticsOfPlatform.objects.all()
    for sp in sp_list:
        yesteerday = sp.date - timedelta(days=1)
        print(yesteerday)
        seven_days_ago = sp.date - timedelta(days=7)
        print(seven_days_ago)
        yesteerday_sp = StatisticsOfPlatform.objects.filter(date=yesteerday)
        if yesteerday_sp and yesteerday_sp[0].dollar_price:
            sp.sametermrate = round(sp.dollar_price/yesteerday_sp[0].dollar_price,4)
        seven_days_ago_sp = StatisticsOfPlatform.objects.filter(date=seven_days_ago)
        if seven_days_ago_sp and seven_days_ago_sp[0].dollar_price:
            sp.weekrate = round(sp.dollar_price/seven_days_ago_sp[0].dollar_price,2)
        sp.save()
