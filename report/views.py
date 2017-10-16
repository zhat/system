from django.shortcuts import render
from django.http import HttpResponseRedirect,Http404
from .models import StatisticsData,StatisticsOfPlatform,ReportData,AmazonProductBaseinfo,ProductStock
from django.contrib.auth.decorators import login_required
from datetime import datetime,timedelta
import pandas as pd

# Create your views here.

@login_required
def index(request):
    """
    :param request:
    :return:
    有开始时间
       有结束时间
           判断结束时间是否大于开始时间30天
           没有大于30天 按结束时间 大于30天报错
       没有结束时间
           判断开始时间30天后和今天前两天，取小值
    没有开始时间
       有结束时间
           开始时间为结束时间的前37天
       没有结束时间
           显示最近一个月数据 今天前2天到今天前39天
    """
    start = request.GET.get('start', '').strip()
    end = request.GET.get('end', '').strip()
    if start:           #有开始时间
        start_date = datetime.strptime(start, '%Y-%m-%d')
        start = start_date - timedelta(days=7)
        start = start.strftime('%Y-%m-%d')
        if end:
            end_date = start_date - timedelta(days=-30)  # 开始时间30天后
            end = datetime.strptime(end, '%Y-%m-%d')
            end = end_date if end_date<end else end
        else:
            now = datetime.now()
            end_date = now - timedelta(days=2)          #两天前
            end = start_date-timedelta(days=-30)         #开始时间30天后
            end = end_date if end_date<end else end       #两天前和开始时间30天后中的小值
            end = end.strftime("%Y-%m-%d")
    else:       #没有开始时间
        if end:
            end = datetime.strptime(end, '%Y-%m-%d')
            start = end - timedelta(days=37)
            start = start.strftime("%Y-%m-%d")
            end = end.strftime("%Y-%m-%d")
        else:
            now = datetime.now()
            end = now - timedelta(days=2)
            end = end.strftime("%Y-%m-%d")
            start = now - timedelta(days=39)
            start = start.strftime("%Y-%m-%d")
    days = pd.date_range(start=start, end=end)
    data_frame = pd.DataFrame(0, index=days, columns=['dollar_price', 'weekrate', 'sametermrate'])

    so=StatisticsOfPlatform.objects.filter(date__range=(start,end))
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

@login_required
def product_list(request):
    date = request.GET.get('start', '').strip()
    if not date:
        now = datetime.now()
        the_day_before_yesterday = now - timedelta(days=2)
        date = the_day_before_yesterday.strftime("%Y-%m-%d")
    print(date)
    rd_list = ReportData.objects.filter(date=date).order_by("-price")[:50]
    rd_list = sorted(rd_list,key=lambda rd:rd.weekrate)
    rise_top10 = rd_list[-10:]
    rise_top10.reverse()
    drop_top10 = rd_list[:10]
    return render(request,'report/product_list.html',{'rise_top10':rise_top10,'drop_top10':drop_top10})

@login_required
def product_detail(request):
    asin = request.GET.get('asin', '').strip()
    start = request.GET.get('start', '').strip()
    end = request.GET.get('end','').strip()
    #if asin=="":
    #    raise Http404
    if start:           #有开始时间
        start_date = datetime.strptime(start, '%Y-%m-%d')
        start = start_date - timedelta(days=7)
        start = start.strftime('%Y-%m-%d')
        if end:
            end_date = start_date - timedelta(days=-30)  # 开始时间30天后
            end = datetime.strptime(end, '%Y-%m-%d')
            end = end_date if end_date < end else end
        else:
            now = datetime.now()
            end_date = now - timedelta(days=2)          #两天前
            end = start_date-timedelta(days=-30)         #开始时间30天后
            end = end_date if end_date<end else end       #两天前和开始时间30天后中的小值
            end = end.strftime("%Y-%m-%d")
    else:       #没有开始时间
        if end:
            end = datetime.strptime(end, '%Y-%m-%d')
            start = end - timedelta(days=37)
            start = start.strftime("%Y-%m-%d")
            end = end.strftime("%Y-%m-%d")
        else:
            now = datetime.now()
            end = now - timedelta(days=2)
            end = end.strftime("%Y-%m-%d")
            start = now - timedelta(days=39)
            start = start.strftime("%Y-%m-%d")
    days=pd.date_range(start=start,end=end)
    data_frame = pd.DataFrame(0,index=days,columns=['price','weekrate','sametermrate'])
    if asin:
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

    return render(request,'report/product.html',{'asin':asin,'date_list':date_list,'data_list':data_list,
                                                 'weekrate_list':weekrate_list,'sametermrate_list':sametermrate_list,
                                                 'max_rate':max_rate,'rate_interval':rate_interval,
                                                 'max_price':max_price,'interval':interval})

@login_required
def product_detail_date(request):
    asin = request.GET.get('asin', '').strip()
    date_str = request.GET.get('date', '').strip()
    #if not asin or not date:
    #    raise Http404
    if not date_str:
        now = datetime.now()
        date = now - timedelta(days=2)
    else:
        date = datetime.strptime(date_str, '%Y-%m-%d')
    product_info_list = []
    product_list = []
    product_base = AmazonProductBaseinfo.objects.filter(asin=asin)
    for date in [date,date-timedelta(days=1),date-timedelta(days=7)]:
        start = date
        end = start + timedelta(hours=23, minutes=59, seconds=59)
        date_str = date.strftime("%Y-%m-%d")
        product = ReportData.objects.filter(asin=asin).filter(date=date_str).first()
        product_list.append(product)

        #获取某天的价格、评分和库存
        try:
            product_info = product_base.filter(create_date__range=(start, end)).order_by(
                '-create_date')[0]  #取当天最后一次数据


            product_info_list.append({
                'asin':asin,
                'date':date_str,
                'in_sale_price':product_info.in_sale_price,
                'review_avg_star':product_info.review_avg_star
            })
        except IndexError:
            product_info_list.append({
                 'asin': asin,
                 'date': date_str,
                 'in_sale_price': "",
                 'review_avg_star': ""
             })
        rd_list = ReportData.objects.filter(asin=asin)
        if rd_list:
            sku = rd_list[0].sku
            stock = ProductStock.objects.filter(date=date_str).filter(sku=sku)
            if stock:
                product_info_list[-1]['stock']=stock[0].stock
            else:
                product_info_list[-1]['stock'] = 0
        else:
            product_info_list[-1]['stock'] = 0

    return render(request,'report/product_date.html',{'asin':asin,'product_info_list':product_info_list,
                                                      'product_list':product_list})