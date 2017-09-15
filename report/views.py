from django.shortcuts import render
from .models import StatisticsData,StatisticsOfPlatform,ReportData
# Create your views here.
from django.db import connection, transaction
from datetime import datetime,timedelta

def index(request):
    so=StatisticsOfPlatform.objects.all()[:37]
    date_list = []
    data_list = []
    weekrate_list = []
    sametermrate_list = []
    for s in so:
        date_list.append(s.date.strftime("%Y/%m/%d"))
        data_list.append(float(s.dollar_price))
        weekrate_list.append(round(float(s.weekrate)*100, 2))  # 销售额周环比
        sametermrate_list.append(round(float(s.sametermrate)*100, 2))  # 销售额日环比
    date_list.reverse()
    data_list.reverse()
    weekrate_list.reverse()
    sametermrate_list.reverse()
    print(sametermrate_list)
    print(weekrate_list)

    max_price = (max(data_list) // 10000 + 1) * 10000
    interval = max_price // 10
    max_rate = (max(weekrate_list + sametermrate_list) // 10 + 1) * 10
    rate_interval = max_rate // 10
    return render(request,'report/index.html',{'date_list':date_list,'data_list':data_list,
                                               'weekrate_list': weekrate_list, 'sametermrate_list': sametermrate_list,
                                               'max_rate': max_rate, 'rate_interval': rate_interval,
                                               'max_price': max_price, 'interval': interval})

def date_test(request):
    return render(request,'report/double_date.html',{})

def product_list(request):
    now = datetime.now()
    the_day_before_yesterday = now - timedelta(days=2)
    the_day_before_yesterday = the_day_before_yesterday.strftime("%Y-%m-%d")
    print(the_day_before_yesterday)
    rd_list = ReportData.objects.filter(date=the_day_before_yesterday).order_by("-price")[:50]
    rd_list = sorted(rd_list,key=lambda rd:rd.sametermrate)
    rise_top10 = rd_list[-10:]
    rise_top10.reverse()
    drop_top10 = rd_list[:10]
    return render(request,'report/product_list.html',{'rise_top10':rise_top10,'drop_top10':drop_top10})


def product_detail(request,asin=""):
    if asin=="":
        return 404
    product_list = ReportData.objects.filter(asin=asin).order_by("-date")[:37]
    date_list = []
    data_list = []
    weekrate_list =[]
    sametermrate_list = []
    for product in product_list:
        date_list.append(product.date.strftime("%Y/%m/%d"))     #日期
        data_list.append(round(float(product.price),2))              #销售额
        weekrate_list.append(round(float(product.weekrate)*100,2))       #销售额周环比
        sametermrate_list.append(round(float(product.sametermrate)*100,2))   #销售额日环比

    date_list.reverse()
    data_list.reverse()
    weekrate_list.reverse()
    sametermrate_list.reverse()
    max_price = (max(data_list)//100+1)*100
    max_rate = (max(weekrate_list+sametermrate_list)//100+1)*100
    rate_interval = max_rate//10
    interval = max_price//10
    return render(request,'report/product.html',{'date_list':date_list,'data_list':data_list,
                                                 'weekrate_list':weekrate_list,'sametermrate_list':sametermrate_list,
                                                 'max_rate':max_rate,'rate_interval':rate_interval,
                                                 'max_price':max_price,'interval':interval})