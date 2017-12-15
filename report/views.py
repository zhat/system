from django.shortcuts import render
from django.http import Http404
from .models import StatisticsOfPlatform,ReportData,AmazonProductBaseinfo,CompetitiveProduct,AmazonBusinessReport,AmazonTodayDeal,AmazonDailyInventory
from django.contrib.auth.decorators import login_required
from datetime import datetime,timedelta
import pandas as pd
import re
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
            end = end.strftime("%Y-%m-%d")
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
        if product.dollar_price:
            data_frame.loc[product.date.strftime("%Y-%m-%d"), 'dollar_price'] = round(float(product.dollar_price), 2)
        if product.weekrate:
            data_frame.loc[product.date.strftime("%Y-%m-%d"), 'weekrate'] = round(float(product.weekrate) * 100, 2)
        if product.sametermrate:
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
    date = request.GET.get('date', '').strip()
    if not date:
        now = datetime.now()
        the_day_before_yesterday = now - timedelta(days=2)
        date = the_day_before_yesterday.strftime("%Y-%m-%d")
    print(date)
    rd_list = ReportData.objects.filter(date=date).order_by("-price")[:50]
    """<td>{{ forloop.counter }}
                    <td>{{ product.date }}</td>
                    <td>{{ product.platform }}</td>
                    <td>{{ product.station }}</td>
                    <td>{{ product.qty }}</td>
                    <td>{{ product.count }}</td>
                    <td>{{ product.price }}</td>
                    <td>{{ product.sametermrate }}%</td>
                    <td>{{ product.weekrate }}%</td>
                    <td>{{ product.sku }}</td>
                    <td><a href="{% url 'report:product_detail' %}?asin={{ product.asin }}">{{ product.asin """
    rd_list = [{
                'date':rd.date,
                'platform':rd.platform,
                'station':rd.station,
                'qty':rd.qty,
                'count':rd.count,
                'price':rd.price,
                'sametermrate':round(rd.sametermrate*100,2),
                'weekrate':round(rd.weekrate*100,2),
                'sku':rd.sku,
                'asin':rd.asin
            } for rd in rd_list]
    price_top10 = rd_list[:10]
    rd_list = [rd for rd in rd_list if rd['weekrate']]
    rd_list = sorted(rd_list,key=lambda rd:rd['weekrate'])
    rise_top10 = rd_list[-10:]
    rise_top10.reverse()
    drop_top10 = rd_list[:10]
    return render(request,'report/product_list.html',{'date':date,'price_top10':price_top10,
                                                      'rise_top10':rise_top10,'drop_top10':drop_top10})

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
    zone = "US"
    product_asin = request.GET.get('asin', '').strip()
    date_str = request.GET.get('date', '').strip()
    #if not asin or not date:
    #    raise Http404
    if not date_str:                            #如果没有输入日期 就默认显示现在日期前两天的数据
        now = datetime.now()
        date = now - timedelta(days=2)
    else:
        date = datetime.strptime(date_str, '%Y-%m-%d')

    asin_list = [product_asin]
    competitor = CompetitiveProduct.objects.filter(zone__iexact=zone,asin=product_asin).first()  #filter(zone__iexact=zone)
    if competitor and competitor.competitive_product_asin:
        asin_list.append(competitor.competitive_product_asin)   #获取竞品asin 加入asin list中

    date_list = [date,date-timedelta(days=1),date-timedelta(days=7)] #分别获取当天 前一天 上周同一天日期
    product_list = []
    for date in date_list:
        date_str = date.strftime("%Y-%m-%d")
        product = ReportData.objects.filter(asin=product_asin).filter(date=date_str).first()
        if product:
            product_list.append({
                'date': product.date.strftime('%Y-%m-%d'),
                'asin': product.asin,
                'platform': product.platform,
                'station': product.station,
                'qty': product.qty,
                'count': product.count,
                'currencycode': product.currencycode,
                'price': product.price,
                'sametermrate': '%.2f%%'%(product.sametermrate*100),
                'weekrate': '%.2f%%'%(product.weekrate*100)
            })

    tuples = [(asin, date.strftime("%Y-%m-%d"))
              for asin in asin_list for date in date_list]
    index = pd.MultiIndex.from_tuples(tuples, names=['asin', '日期'])
    #columns = ['in_sale_price', 'review_avg_star', 'stock', 'sessions','session_percentage',
    #           'total_order_items','conversion_rate','buy_box','today_deal_index','today_deal_type']
    columns = ['单价', '评分', '库存', '流量', '转化率', 'buy_box', 'deal排名', 'deal类型']
    data_frame = pd.DataFrame(None, index=index, columns=columns)
    print(data_frame)
    print(data_frame.T)
    analytic_result = []
    for asin in asin_list:
        #获取某天的价格、评分和库存
        for date in date_list:
            start = date
            end = start + timedelta(hours=23, minutes=59, seconds=59)
            date_str = date.strftime("%Y-%m-%d")
            product_base = AmazonProductBaseinfo.objects.filter(asin=asin).exclude(brand_url="Unknown")
            product_info_list = product_base.filter(create_date__range=(start, end)).order_by(
                '-create_date')  #取当天最后一次数据
            print(product_info_list)
            if product_info_list:
                product_info = product_info_list[0]
                data_frame.loc[(asin, date_str), '单价'] = product_info.lowest_price
                data_frame.loc[(asin, date_str), '评分'] = product_info.review_avg_star

                if product_info.stock_situation == "In Stock.":
                    stock_situation = product_info.stock_situation
                elif product_info.stock_situation == "":
                    stock_situation = "NULL"
                elif re.findall(r'Only 5 left in stock',product_info.stock_situation):
                    num = re.findall(r'Only (\d{1,2}) left in stock', product_info.stock_situation)
                    stock_situation = num[0]
                else:
                    stock_situation = "无库存"
                data_frame.loc[(asin, date_str), '库存'] = stock_situation
            if asin == product_asin:        #如果asin是公司产品asin 则取出详细库存显示
                amazon_daily = AmazonDailyInventory.objects.using("sellerreport").\
                    filter(zone__iexact=zone.lower()).\
                    filter(data_date=date_str).\
                    filter(asin=asin).first()
                if amazon_daily:
                    data_frame.loc[(asin, date_str), '库存'] = amazon_daily.afn_fulfillable_quantity
                else:
                    data_frame.loc[(asin, date_str), '库存'] = 0

            print(zone,asin,date_str)
            business_report = AmazonBusinessReport.objects.using("sellerreport").\
                filter(zone__iexact=zone.lower()).filter(child_asin=asin).filter(data_date=date_str).first()
            if business_report:
                data_frame.loc[(asin, date_str), '流量'] = business_report.sessions
                if business_report.sessions:
                    data_frame.loc[(asin, date_str), '转化率'] ="{}%".format(
                        round((business_report.total_order_items/business_report.sessions)*100,2))
                else:
                    data_frame.loc[(asin,date_str), '转化率'] = 0
                data_frame.loc[(asin, date_str), 'buy_box'] = business_report.buy_box

            today_deal = AmazonTodayDeal.objects.filter(zone__iexact=zone.lower()).filter(asin=asin).filter(date=date_str).first()
            if today_deal:
                today_deal_index = (today_deal.page-1)*48 + today_deal.page_index + 1
                data_frame.loc[(asin, date_str), 'deal排名'] = today_deal_index
                data_frame.loc[(asin, date_str), 'deal类型'] = today_deal.deal_type

                #排名 类型

    data_list = data_frame.T.to_csv().split('\n')
    product_info_list = [data.split(',') for data in data_list if data]
    product_info_thead = product_info_list[1]
    product_info_tbody = product_info_list[2:]
    return render(request,'report/product_date.html',{'asin':asin_list[0],'asin_list':asin_list,
                                                      'product_info_thead':product_info_thead,
                                                      "product_info_tbody":product_info_tbody,
                                                      'product_list':product_list})