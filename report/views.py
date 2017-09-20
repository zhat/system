from django.shortcuts import render
from django.http import HttpResponseRedirect,Http404
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from .models import StatisticsData,StatisticsOfPlatform,ReportData
# Create your views here.
from django.db import connection, transaction
from datetime import datetime,timedelta
import time
import pandas as pd

def index(request):
    now = datetime.now()
    day_before_yesterday = now - timedelta(days=2)
    day_before_yesterday = day_before_yesterday.strftime("%Y-%m-%d")
    days_date = now - timedelta(days=39)
    days_date = days_date.strftime("%Y-%m-%d")
    days = pd.date_range(start=days_date, end=day_before_yesterday)
    data_frame = pd.DataFrame(0, index=days, columns=['dollar_price', 'weekrate', 'sametermrate'])

    so=StatisticsOfPlatform.objects.all()[:37]
    for product in so:
        data_frame.loc[product.date.strftime("%Y-%m-%d"), 'dollar_price'] = round(float(product.dollar_price), 2)
        data_frame.loc[product.date.strftime("%Y-%m-%d"), 'weekrate'] = round(float(product.weekrate) * 100, 2)
        data_frame.loc[product.date.strftime("%Y-%m-%d"), 'sametermrate'] = round(float(product.sametermrate) * 100, 2)

    date_list = [date.strftime("%Y/%m/%d") for date in data_frame.index]
    data_list = [float(value) for value in data_frame['dollar_price'].values]
    weekrate_list = [float(value) for value in data_frame['weekrate'].values]
    sametermrate_list = [float(value) for value in data_frame['sametermrate'].values]
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
    rd_list = ReportData.objects.filter(date=the_day_before_yesterday).order_by("-price")[:50]
    rd_list = sorted(rd_list,key=lambda rd:rd.sametermrate)
    rise_top10 = rd_list[-10:]
    rise_top10.reverse()
    drop_top10 = rd_list[:10]
    return render(request,'report/product_list.html',{'rise_top10':rise_top10,'drop_top10':drop_top10})

def product_detail(request):
    asin = request.GET.get('asin', '').strip()
    start = request.GET.get('start', '').strip()
    end = request.GET.get('end','').strip()
    if asin=="":
        raise Http404
    if start:
        start = datetime.strptime(start,'%Y-%m-%d')
        start = start - timedelta(days=7)
        start = start.strftime('%Y-%m-%d')
    if not start or not end:
        now = datetime.now()
        end = now - timedelta(days=2)
        end = end.strftime("%Y-%m-%d")
        start = now - timedelta(days=39)
        start = start.strftime("%Y-%m-%d")
    days=pd.date_range(start=start,end=end)
    print(days)
    data_frame = pd.DataFrame(0,index=days,columns=['price','weekrate','sametermrate'])
    print(data_frame)
    product_list = ReportData.objects.filter(asin=asin).filter(date__range=(start,end)).order_by("-date")
    if not product_list:
        raise Http404
    for product in product_list:
        data_frame.loc[product.date.strftime("%Y-%m-%d"),'price'] = round(float(product.price),2)
        data_frame.loc[product.date.strftime("%Y-%m-%d"), 'weekrate'] = round(float(product.weekrate)*100,2)
        data_frame.loc[product.date.strftime("%Y-%m-%d"), 'sametermrate'] = round(float(product.sametermrate)*100,2)

    date_list = [date.strftime("%Y/%m/%d") for date in data_frame.index]
    data_list = [float(value) for value in data_frame['price'].values]
    weekrate_list = [float(value) for value in data_frame['weekrate'].values]
    sametermrate_list = [float(value) for value in data_frame['sametermrate'].values]
    max_price = (max(data_list)//100+1)*100
    max_rate = (max(weekrate_list+sametermrate_list)//100+1)*100
    rate_interval = max_rate//10
    interval = max_price//10

    return render(request,'report/product.html',{'date_list':date_list,'data_list':data_list,
                                                 'weekrate_list':weekrate_list,'sametermrate_list':sametermrate_list,
                                                 'max_rate':max_rate,'rate_interval':rate_interval,
                                                 'max_price':max_price,'interval':interval})


def product_detail_date(request):
    asin = request.GET.get('asin', '').strip()
    date = request.GET.get('date', '').strip()
    if not asin or not date:
        raise Http404
    a = time.strptime(date,'%Y%m%d')
    date = datetime(*a[:3]).strftime("%Y-%m-%d")
    return render(request,'report/product_date.html',{'asin':asin,'date':date})