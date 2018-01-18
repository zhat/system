from django.shortcuts import render
from django.http import Http404
from .models import StatisticsOfPlatform,ReportData,AmazonProductBaseinfo,CompetitiveProduct,AmazonDailyInventory
from .models import AmazonProductCategorySalesRank,AmazonBusinessReport,AmazonTodayDeal
from django.contrib.auth.decorators import login_required
from datetime import datetime,timedelta
import pandas as pd
from django.db.models import Q
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
    zone = request.GET.get('zone','').strip()
    if not zone:
        zone = "US"
    start = request.GET.get('start', '').strip()
    end = request.GET.get('end', '').strip()
    zone_list = ["US","DE","CA","JP","UK","ES","FR","IT"]
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

    so=StatisticsOfPlatform.objects.filter(date__range=(start,end)).filter(platform=zone)
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
    max_rate = (max(weekrate_list + sametermrate_list) // 100 + 1) * 100
    rate_interval = (max_rate+100) // 10
    return render(request,'report/index.html',{'date_list':date_list,'data_list':data_list,'zone_list':zone_list,'zone':zone,
                                               'weekrate_list': weekrate_list, 'sametermrate_list': sametermrate_list,
                                               'max_rate': max_rate, 'rate_interval': rate_interval,
                                               'max_price': max_price, 'interval': interval})

def date_test(request):
    return render(request,'report/double_date.html',{})

@login_required
def product_list(request):
    date = request.GET.get('date', '').strip()
    zone = request.GET.get('zone', 'US').strip()
    zone_list = ["US","DE","CA","JP","UK","ES","FR","IT"]
    if not date:
        now = datetime.now()
        the_day_before_yesterday = now - timedelta(days=2)
        date = the_day_before_yesterday.strftime("%Y-%m-%d")
    # print(date)
    rd_list = ReportData.objects.filter(date=date,platform=zone).order_by("-price")[:50]
    price_top10 = rd_list[:10]
    price_top10 = to_dict(price_top10)

    rd_list = [rd for rd in rd_list if rd.weekrate != 1]
    rd_list = sorted(rd_list,key=lambda rd:rd.weekrate)
    rise_top10 = [rd for rd in rd_list if rd.weekrate>0][-10:]
    rise_top10.reverse()
    rise_top10 = to_dict(rise_top10)
    drop_top10 = [rd for rd in rd_list if rd.weekrate<0 and rd.weekrate>-1][:10]
    drop_top10 = to_dict(drop_top10)
    return render(request,'report/product_list.html',{'date':date,'price_top10':price_top10,'zone':zone,
                                                      'zone_list':zone_list,
                                                      'rise_top10':rise_top10,'drop_top10':drop_top10})

def to_dict(rd_list):
    return [{
        'date': rd.date,
        'platform': rd.platform,
        'station': rd.station,
        'qty': rd.qty,
        'count': rd.count,
        'price': rd.price,
        'sametermrate': round(rd.sametermrate * 100, 2),
        'weekrate': round(rd.weekrate * 100, 2),
        'sku': rd.sku,
        'asin': rd.asin
    } for rd in rd_list]

@login_required
def product_detail(request):
    zone = request.GET.get('zone','US').strip()
    asin = request.GET.get('asin', '').strip()
    start = request.GET.get('start', '').strip()
    end = request.GET.get('end','').strip()
    zone_list = ["US", "DE", "CA", "JP", "UK", "ES", "FR", "IT"]
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
        product_list = ReportData.objects.filter(asin=asin,platform=zone).filter(date__range=(start,end)).order_by("-date")
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
    rate_interval = (max_rate+100)//10
    interval = max_price//10

    return render(request,'report/product.html',{'asin':asin,'date_list':date_list,'data_list':data_list,
                                                 'zone':zone,'zone_list':zone_list,
                                                 'weekrate_list':weekrate_list,'sametermrate_list':sametermrate_list,
                                                 'max_rate':max_rate,'rate_interval':rate_interval,
                                                 'max_price':max_price,'interval':interval})

@login_required
def product_detail_date(request):
    zone = request.GET.get('zone','US').strip()
    zone_list = ["US", "DE", "CA", "JP", "UK", "ES", "FR", "IT"]
    product_asin = request.GET.get('asin', '').strip()
    date_str = request.GET.get('date', '').strip()
    if not zone:
        zone = "US"
    #if not asin or not date:
    #    raise Http404
    if not date_str:                            #如果没有输入日期 就默认显示现在日期前两天的数据
        now = datetime.now()
        date_str = (now - timedelta(days=2)).strftime('%Y-%m-%d')
    date = datetime.strptime(date_str, '%Y-%m-%d')

    asin_list = [product_asin]
    competitor = CompetitiveProduct.objects.filter(Q(zone=zone)|Q(zone=zone.lower())).filter(asin=product_asin).first()  #filter(zone__iexact=zone)
    if competitor and competitor.competitive_product_asin:
        asin_list.append(competitor.competitive_product_asin)   #获取竞品asin 加入asin list中

    date_list = [date,date-timedelta(days=1),date-timedelta(days=7)] #分别获取当天 前一天 上周同一天日期
    columns = ['asin','platform','station','qty','count','currencycode','price','sametermrate','weekrate']
    data_frame = pd.DataFrame(None,index = date_list ,columns=columns)
    for date in date_list:
        date_str = date.strftime("%Y-%m-%d")
        product = ReportData.objects.filter(asin=product_asin,platform=zone).filter(date=date_str).first()
        if product:
            data_frame.loc[date, 'asin'] = product.asin
            data_frame.loc[date, 'platform'] = product.platform
            data_frame.loc[date, 'station'] = product.station
            data_frame.loc[date, 'qty'] = product.qty
            data_frame.loc[date, 'count'] = product.count
            data_frame.loc[date, 'currencycode'] = product.currencycode
            data_frame.loc[date, 'price'] = product.price
            data_frame.loc[date, 'sametermrate'] = '%.2f%%'%(product.sametermrate*100)
            data_frame.loc[date, 'weekrate'] = '%.2f%%'%(product.weekrate*100)
    data_list = data_frame.to_csv().split('\n')
    product_list = [data.split(',') for data in data_list if data][1:]

    tuples = [(asin, date.strftime("%Y-%m-%d"))
              for asin in asin_list for date in date_list]
    index = pd.MultiIndex.from_tuples(tuples, names=['asin', '日期'])
    #columns = ['in_sale_price', 'review_avg_star', 'stock', 'sessions','session_percentage',
    #           'total_order_items','conversion_rate','buy_box','today_deal_index','today_deal_type']
    columns = ['单价', '评分', '库存', '流量', '转化率', 'buy_box', 'deal排名', 'deal类型','销售排名类名名称','销售排名']
    data_frame = pd.DataFrame(None, index=index, columns=columns)
    # print(data_frame)
    # print(data_frame.T)
    analytic_result = []
    for asin in asin_list:
        #获取某天的价格、评分和库存
        for date in date_list:
            start = date
            end = start + timedelta(hours=23, minutes=59, seconds=59)
            date_str = date.strftime("%Y-%m-%d")
            product_info_list = AmazonProductBaseinfo.objects.using('front').\
                filter(asin=asin).filter(Q(zone=zone)|Q(zone=zone.lower())).\
                filter(create_date__range=(start, end)).\
                exclude(in_sale_price=0).order_by('-create_date')
            # print(product_info_list.query)
            # print(product_info_list)
            if product_info_list:
                product_info = product_info_list[0]
                data_frame.loc[(asin, date_str), '单价'] = product_info.lowest_price
                data_frame.loc[(asin, date_str), '评分'] = product_info.review_avg_star

                if product_info.stock_situation == "In Stock.":
                    stock_situation = "有"
                elif product_info.stock_situation == "":
                    stock_situation = "NULL"
                elif re.findall(r'Only 5 left in stock',product_info.stock_situation):
                    num = re.findall(r'Only (\d{1,2}) left in stock', product_info.stock_situation)
                    stock_situation = "有"
                else:
                    stock_situation = "无"
                data_frame.loc[(asin, date_str), '库存'] = stock_situation
            if asin == product_asin:        #如果asin是公司产品asin 则取出详细库存显示
                amazon_daily = AmazonDailyInventory.objects.using("sellerreport").\
                    filter(Q(sub_zone=zone)|Q(sub_zone=zone.lower())).\
                    filter(data_date=date_str).\
                    filter(asin=asin).first()
                if amazon_daily:
                    data_frame.loc[(asin, date_str), '库存'] = amazon_daily.afn_fulfillable_quantity
                else:
                    data_frame.loc[(asin, date_str), '库存'] = None

            # print(zone,asin,date_str)
            business_report = AmazonBusinessReport.objects.using("sellerreport"). \
                filter(Q(zone=zone) | Q(zone=zone.lower())).filter(child_asin=asin).filter(data_date=date_str).first()
            if business_report:
                data_frame.loc[(asin, date_str), '流量'] = business_report.sessions
                if business_report.sessions:
                    data_frame.loc[(asin, date_str), '转化率'] ="{}%".format(
                        round((business_report.total_order_items/business_report.sessions)*100,2))
                else:
                    data_frame.loc[(asin,date_str), '转化率'] = 0
                data_frame.loc[(asin, date_str), 'buy_box'] = business_report.buy_box

            today_deal = AmazonTodayDeal.objects.using('front'). \
                filter(Q(zone=zone) | Q(zone=zone.lower())).\
                filter(asin=asin).filter(date=date_str).first()
            if today_deal:
                today_deal_index = (today_deal.page-1)*48 + today_deal.page_index + 1
                data_frame.loc[(asin, date_str), 'deal排名'] = today_deal_index
                data_frame.loc[(asin, date_str), 'deal类型'] = today_deal.deal_type

            #排名 类型
            date_format = r'DATE_FORMAT(create_date,"%%Y-%%m-%%d")'
            acsr = AmazonProductCategorySalesRank.objects.using('front'). \
                extra(select={'date': date_format}, where={'{}="{}"'.format(date_format, date_str)}). \
                filter(Q(zone=zone) | Q(zone=zone.lower())).filter(asin=asin, category_name__contains="(See Top 100"). \
                order_by('sales_rank').first()
            if acsr:
                data_frame.loc[(asin, date_str), '销售排名类名名称'] = acsr.category_name.replace("(See Top 100","")
                data_frame.loc[(asin, date_str), '销售排名'] = acsr.sales_rank

    data_list = data_frame.T.to_csv().split('\n')
    product_info_list = [data.split(',') for data in data_list if data]
    product_info_thead = product_info_list[1]
    product_info_tbody = product_info_list[2:]
    # 分析库存 哪个天没有库存

    # 以周环比分析销售变化情况，上升，下降，持平
    has_competitor = True if len(asin_list) > 1 else False
    weekrate = product_list[0][-1]
    result_list = []
    if weekrate:
        weekrate = float(weekrate[:-1])
        if weekrate < 0:
            result_list.append("销量比较上周下降了{:.2f}%".format(abs(weekrate)))
            result_list += analyse(product_info_tbody,0,has_competitor)
        elif weekrate == 0:
            result_list.append("销量与上周相比持平")
        else:
            result_list.append("销量比较上周上升了{:.2f}%".format(abs(weekrate)))
            result_list += analyse(product_info_tbody, 1, has_competitor)
    else:
        result_list = ["当日没有销售数据"]


    return render(request,'report/product_date.html',{'asin':asin_list[0],'asin_list':asin_list,
                                                      'zone':zone,'zone_list':zone_list,
                                                      'product_info_thead':product_info_thead,
                                                      "product_info_tbody":product_info_tbody,
                                                      'product_list':product_list,'result_list':result_list})

def analyse(product_info,scope,has_competitor):
    result_str_list = []
    UP = True
    DOWN = False
    if scope:  #上升
        # 是不是上周没有库存,如果有竞品，竞品是不是没有库存
        stocks = product_info[2]
        today_stock = stocks[1]
        last_week_stock = stocks[3]
        stock_str = []
        if today_stock and not last_week_stock:
            stock_str.append("上周没有库存")
        if today_stock and has_competitor and stocks[4] == "无":
            stock_str.append("竞品没有库存")
        stock_str = ','.join(stock_str)
        if stock_str:
            result_str_list.append(stock_str)
        # 是不是今天上了deal 上周没有上，如果有竞品，竞品是不是没有上deal
        deal_index_list = product_info[6]
        today_deal_index = deal_index_list[1]
        last_week_deal_index = deal_index_list[3]
        deal_str = []
        if today_deal_index and not last_week_deal_index:
            deal_str.append("当天有上deal,上周没有上deal")
        deal_str = ','.join(deal_str)
        if deal_str:
            result_str_list.append(deal_str)
        # 价格与上周相比是不是下降了，如果有竞品，竞品价格是不是上涨了
        prices = product_info[0]
        price_str = []
        result = compare(prices[1], prices[3], attr="本商品价格", scope=DOWN)
        if result:
            price_str.append(result)
        if has_competitor:
            result = compare(prices[4], prices[6], attr="竞品价格", scope=UP)
            if result:
                price_str.append(result)

        price_str = ','.join(price_str)
        if price_str:
            result_str_list.append(price_str)
        # 评分是不是上升了，如果有竞品，竞品评分是不是下降了
        review_avg_score = product_info[1]
        score_str = []
        result = compare(review_avg_score[1], review_avg_score[3], attr="本商品评分", scope=UP)
        if result:
            score_str.append(result)
        if has_competitor:
            result = compare(review_avg_score[4], review_avg_score[6], attr="竞品评分", scope=DOWN)
            if result:
                score_str.append(result)
        score_str = ','.join(score_str)
        if score_str:
            result_str_list.append(score_str)

        # buybox （今天-上周）/上周>5%
        buyboxs = product_info[5]
        buybox_str = compare(buyboxs[1], buyboxs[3], attr="buybox", scope=UP)
        if buybox_str:
            result_str_list.append(buybox_str)
        # 转化率 （今天-上周）/上周>5%
        conve_rates = product_info[4]
        conve_str = compare(conve_rates[1], conve_rates[3], attr="转化率", scope=UP)
        if conve_str:
            result_str_list.append(conve_str)
    else:  #下降
        # 是否有库存
        stocks = product_info[2]
        today_stock = stocks[1]
        last_week_stock = stocks[3]
        stock_str = ''
        if not today_stock:
            stock_str = "该商品当天没有库存"
        if stock_str:
            result_str_list.append(stock_str)
        # 是否是因为今天没有上deal 上周上了deal 如果有竞品，竞品是否上了deal
        deal_index_list = product_info[6]
        today_deal_index = deal_index_list[1]
        last_week_deal_index = deal_index_list[3]
        deal_str = []
        if not today_deal_index and last_week_deal_index:
            deal_str.append("上周上了deal，当天没有上deal")
        if not today_deal_index and has_competitor and deal_index_list[4]:
            deal_str.append("本商品没有上deal，竞品上了deal")
            deal_str = ','.join(deal_str)
            if deal_str:
                result_str_list.append(deal_str)

        # 价格与上周相比是否加价了，如果有竞品，竞品是否降价了
        prices = product_info[0]
        price_str = []
        result = compare(prices[1], prices[3], attr="本商品价格", scope=UP)
        if result:
            price_str.append(result)
        if has_competitor:
            result = compare(prices[4], prices[6], attr="竞品价格", scope=DOWN)
            if result:
                    price_str.append(result)
        price_str = ','.join(price_str)
        if price_str:
                result_str_list.append(price_str)

        # 评分是否下降了，如果有竞品，竞品的评分是否上升了
        review_avg_score = product_info[1]
        score_str = []
        result = compare(review_avg_score[1], review_avg_score[3], attr="本商品评分", scope=DOWN)
        if result:
            score_str.append(result)
        if has_competitor:
            result = compare(review_avg_score[4], review_avg_score[6], attr="竞品评分", scope=UP)
            if result:
                score_str.append(result)
        score_str = ','.join(score_str)
        if score_str:
            result_str_list.append(score_str)

        # buybox （今天-上周）/上周<-5%
        buyboxs = product_info[5]
        buybox_str = compare(buyboxs[1], buyboxs[3], attr="buybox", scope=DOWN)
        if buybox_str:
            result_str_list.append(buybox_str)

        # 转化率 （今天-上周）/上周<-5%
        conve_rates = product_info[4]
        conve_str = compare(conve_rates[1], conve_rates[3], attr="转化率", scope=DOWN)
        if conve_str:
            result_str_list.append(conve_str)

    return result_str_list

def compare(today,last_week,attr="",scope=True):
    if today and last_week:
        # print(today,last_week)
        is_percent = False      #是否含有"%"
        if "%" == today[-1]:
            is_percent = True
            today = today[:-1]
        if "%" == last_week[-1]:
            is_percent = True
            last_week = last_week[:-1]
        today = float(today)
        last_week = float(last_week)
        if last_week == 0:      #上周为0 不能进行除法运算
            return ""
        change = today - last_week
        rate = change/last_week
        # print(attr,change,rate,today,last_week)
        if is_percent and abs(rate)<0.05:
            return ""
        if scope and change>0:   #上升
            trend1 = "增加"
            trend2 = "上升"
            if "价格" in attr:
                trend1 = "上调"
                trend2 = "上调"
        elif not scope and change<0:
            trend1 = "减少"
            trend2 = "下降"
            if "价格" in attr:
                trend1 = "下调"
                trend2 = "下调"
        else:
            return ""
        if is_percent:
            return "{}{}了{:.2f}%，{}幅度为{:.2%}".format(attr, trend1, abs(change), trend2, abs(rate))
        else:
            return "{}{}了{:.2f}，{}幅度为{:.2%}".format(attr, trend1, abs(change), trend2, abs(rate))
    return ""

def get_data(request):
    zone = request.GET.get('zone', 'US').strip()
    zone_list = ["US", "DE", "CA", "JP", "UK", "ES", "FR", "IT"]
    asin = request.GET.get('asin', '').strip()
    date_str = request.GET.get('date', '').strip()
    column = request.GET.get('column', '').strip()
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")
    end = date_str
    start = (datetime.strptime(end,"%Y-%m-%d")-timedelta(days=30)).strftime("%Y-%m-%d")
    data_frame = get_data_with_column(zone,asin,start,end,column)
    date_list = [date.strftime("%Y-%m-%d") for date in pd.date_range(start=start,end=end)]
    column_data = [float(value) for value in data_frame[column].values]
    max_value = (int(max(column_data)/10)+3)*10
    interval = max_value/5
    if column == "review_avg_star":
        max_value = 5
        interval = 1
    column_dict = {
        "in_sale_price":"单价",
        "review_avg_star":"评分",
        "stock":"库存",
        "sessions":"流量",
        "conversion_rate":"转化率",
        "buy_box":"buy_box",
        "today_deal_index":"deal排名",
        "sale_index":"销售排名"
    }
    column_name = column_dict.get(column,"")
    return render(request,"report/data.html",{"max_value":max_value,'interval':interval,
                                              'zone':zone,'asin':asin,'column':column_name,
                                              "date_list":date_list,"data_list":column_data})

def get_data_with_column(zone,asin,start,end,column):
    # columns = ['in_sale_price', 'review_avg_star', 'stock', 'sessions','session_percentage',
    #           'total_order_items','conversion_rate','buy_box','today_deal_index','today_deal_type']
    date_list = pd.date_range(start=start, end=end)
    # print(date_list)
    data_frame = pd.DataFrame(0, index=date_list, columns=[column])
    if column == "in_sale_price":  #单价
        date_format = r'DATE_FORMAT(create_date,"%%Y-%%m-%%d")'
        product_info_list = AmazonProductBaseinfo.objects.using('front').\
            extra(select={'date':date_format},where={'{} between "{}" and "{}"'.format(date_format,start,end)}).\
            values('in_sale_price','date'). \
            filter(asin=asin).filter(Q(zone=zone) | Q(zone=zone.lower())). \
            exclude(in_sale_price=0).distinct()
        for product_info in product_info_list:
            data_frame.loc[(product_info['date']), column] = product_info['in_sale_price']
    elif column == "review_avg_star": #评分
        date_format = r'DATE_FORMAT(create_date,"%%Y-%%m-%%d")'
        product_info_list = AmazonProductBaseinfo.objects.using('front'). \
            extra(select={'date': date_format}, where={'{} between "{}" and "{}"'.format(date_format, start, end)}). \
            values('review_avg_star', 'date'). \
            filter(asin=asin).filter(Q(zone=zone) | Q(zone=zone.lower())). \
            exclude(in_sale_price=0).distinct()
        for product_info in product_info_list:
            data_frame.loc[(product_info['date']), column] = product_info['review_avg_star']
    elif column == "stock": #库存
        amazon_daily_list = AmazonDailyInventory.objects.using("sellerreport").values('afn_fulfillable_quantity','data_date'). \
            filter(Q(sub_zone=zone) | Q(sub_zone=zone.lower())). \
            filter(data_date__range=(start,end)). \
            filter(asin=asin).order_by('afn_fulfillable_quantity')
        for amazon_daily in amazon_daily_list:
            data_frame.loc[(amazon_daily['data_date']), column] = amazon_daily['afn_fulfillable_quantity']
    elif column == "sessions": #流量
        business_report_list = AmazonBusinessReport.objects.using("sellerreport").values('sessions','data_date'). \
            filter(Q(zone=zone) | Q(zone=zone.lower())).filter(child_asin=asin).filter(data_date__range=(start,end))
        for business_report in business_report_list:
            data_frame.loc[business_report['data_date'], column] = business_report['sessions']

    elif column == "conversion_rate":   #转化率
        business_report_list = AmazonBusinessReport.objects.using("sellerreport").\
            values('total_order_items', 'sessions', 'data_date'). \
            filter(Q(zone=zone) | Q(zone=zone.lower())).filter(child_asin=asin).filter(data_date__range=(start, end))
        for business_report in business_report_list:
            if business_report['sessions']!=0:
                data_frame.loc[business_report['data_date'], column] = round((business_report['total_order_items'] / business_report['sessions']) * 100, 2)
    elif column == "buy_box":
        business_report_list = AmazonBusinessReport.objects.using("sellerreport").values('buy_box', 'data_date'). \
            filter(Q(zone=zone) | Q(zone=zone.lower())).filter(child_asin=asin).filter(data_date__range=(start, end))
        for business_report in business_report_list:
            data_frame.loc[business_report['data_date'], column] = business_report['buy_box'][:-1]

    elif column == "today_deal_index":  #deal排名
        today_deal_list = AmazonTodayDeal.objects.using('front').values('date','page','page_index'). \
            filter(Q(zone=zone) | Q(zone=zone.lower())). \
            filter(asin=asin).filter(date__range=(start,end)).order_by('-page','-page_index')
        for today_deal in today_deal_list:
            today_deal_index = (today_deal.page - 1) * 48 + today_deal.page_index + 1
            data_frame.loc[today_deal['date'], column] = today_deal_index

    elif column == "sale_index":    #销售排名
        date_format = r'DATE_FORMAT(create_date,"%%Y-%%m-%%d")'
        acsr_list = AmazonProductCategorySalesRank.objects.using('front'). \
            extra(select={'date': date_format}, where={'{} between "{}" and "{}"'.format(date_format, start, end)}).\
            values('date','sales_rank'). \
            filter(Q(zone=zone) | Q(zone=zone.lower())).\
            filter(asin=asin, category_name__contains="(See Top 100"). \
            order_by('-sales_rank')
        for acsr in acsr_list:
            data_frame.loc[acsr['date'], column] = acsr['sales_rank']

    return  data_frame