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
    max_rate = (max(weekrate_list + sametermrate_list) // 100 + 1) * 100
    rate_interval = (max_rate+100) // 10
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
    # print(date)
    rd_list = ReportData.objects.filter(date=date).order_by("-price")[:50]
    price_top10 = rd_list[:10]
    price_top10 = to_dict(price_top10)

    rd_list = [rd for rd in rd_list if rd.weekrate != 1]
    rd_list = sorted(rd_list,key=lambda rd:rd.weekrate)
    rise_top10 = [rd for rd in rd_list if rd.weekrate>0][-10:]
    rise_top10.reverse()
    rise_top10 = to_dict(rise_top10)
    drop_top10 = [rd for rd in rd_list if rd.weekrate<0 and rd.weekrate>-1][:10]
    drop_top10 = to_dict(drop_top10)
    return render(request,'report/product_list.html',{'date':date,'price_top10':price_top10,
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
    rate_interval = (max_rate+100)//10
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
    columns = ['asin','platform','station','qty','count','currencycode','price','sametermrate','weekrate']
    data_frame = pd.DataFrame(None,index = date_list ,columns=columns)
    for date in date_list:
        date_str = date.strftime("%Y-%m-%d")
        product = ReportData.objects.filter(asin=product_asin).filter(date=date_str).first()
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
    columns = ['单价', '评分', '库存', '流量', '转化率', 'buy_box', 'deal排名', 'deal类型']
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
                filter(asin=asin).\
                filter(create_date__range=(start, end)).\
                exclude(brand_url="Unknown").order_by('-create_date')
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
                    filter(zone__iexact=zone.lower()).\
                    filter(data_date=date_str).\
                    filter(asin=asin).first()
                if amazon_daily:
                    data_frame.loc[(asin, date_str), '库存'] = amazon_daily.afn_fulfillable_quantity
                else:
                    data_frame.loc[(asin, date_str), '库存'] = None

            # print(zone,asin,date_str)
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

            today_deal = AmazonTodayDeal.objects.using('front').\
                filter(zone__iexact=zone.lower()).\
                filter(asin=asin).filter(date=date_str).first()
            if today_deal:
                today_deal_index = (today_deal.page-1)*48 + today_deal.page_index + 1
                data_frame.loc[(asin, date_str), 'deal排名'] = today_deal_index
                data_frame.loc[(asin, date_str), 'deal类型'] = today_deal.deal_type

                #排名 类型

    data_list = data_frame.T.to_csv().split('\n')
    product_info_list = [data.split(',') for data in data_list if data]
    product_info_thead = product_info_list[1]
    product_info_tbody = product_info_list[2:]
    # 分析库存 哪个天没有库存

    # 以周环比分析销售变化情况，上升，下降，持平
    has_competitor = True if len(asin_list) > 1 else False
    weekrate = product_list[0][-1][:-1]
    result_list = []
    if weekrate:
        weekrate = float(weekrate)
        if weekrate < 0:
            result_list = analyse(product_info_tbody,0,has_competitor)
        elif weekrate == 0:
            result_list.append("销量与上周相比持平")
        else:
            result_list = analyse(product_info_tbody, 1, has_competitor)
    else:
        result_list = ["当日没有销售数据"]


    return render(request,'report/product_date.html',{'asin':asin_list[0],'asin_list':asin_list,
                                                      'product_info_thead':product_info_thead,
                                                      "product_info_tbody":product_info_tbody,
                                                      'product_list':product_list,'result_list':result_list})

def analyse(product_info,scope,has_competitor):
    result_str_list = []
    if scope:  #上升
        result_str_list.append('销量比较上周上升')
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
            deal_str.append("今天上了deal,上周没有上deal")
        if today_deal_index and has_competitor and not deal_index_list[4]:
            deal_str.append("竞品没有上deal")
        deal_str = ','.join(deal_str)
        if deal_str:
            result_str_list.append(deal_str)
        # 价格与上周相比是不是下降了，如果有竞品，竞品价格是不是上涨了
        prices = product_info[0]
        today_price = prices[1]
        last_week_price = prices[3]
        price_str = []
        if today_price and last_week_price and today_price<last_week_price:
            price_str.append("价格与上周相比下降了")
        if has_competitor:
            competitor_today_price = prices[4]
            competitor_last_week_price = prices[6]
            if competitor_today_price and competitor_last_week_price and competitor_today_price>competitor_last_week_price:
                price_str.append("竞品价格上升了")

        price_str = ','.join(price_str)
        if price_str:
            result_str_list.append(price_str)
        # 评分是不是上升了，如果有竞品，竞品评分是不是下降了
        review_avg_score = product_info[1]
        today_score = review_avg_score[1]
        last_week_score = review_avg_score[3]
        score_str = []
        if today_score and last_week_score and today_score>last_week_score:
            score_str.append("评分升高了")
        if has_competitor:
            competitor_today_score = review_avg_score[4]
            competitor_last_week_score = review_avg_score[6]
            if competitor_today_score and competitor_last_week_score and competitor_today_score<competitor_last_week_score:
                score_str.append("竞品评分降低了")
        score_str = ','.join(score_str)
        if score_str:
            result_str_list.append(score_str)
        # buybox （今天-上周）/上周>5%
        buyboxs = product_info[5]
        today_buybox = buyboxs[1]
        last_week_buybox = buyboxs[3]
        buybox_str = ""
        if today_buybox and last_week_buybox:
            today_buybox = float(today_buybox[:-1])
            last_week_buybox = float(last_week_buybox[:-1])
            if last_week_buybox != 0:
                rate = (today_buybox-last_week_buybox)/last_week_buybox
                if rate>0.05:
                    buybox_str = "buybox上升了%.2f%%以上"%(rate*100)
        if buybox_str:
            result_str_list.append(buybox_str)
        # 转化率 （今天-上周）/上周>5%
        conve_rates = product_info[4]
        today_conve = conve_rates[1]
        last_week_conve = conve_rates[3]
        conve_str = ''
        if today_conve and last_week_conve:
            today_conve = float(today_conve[:-1])
            last_week_conve = float(last_week_conve[:-1])
            if last_week_conve != 0:
                rate = (today_conve-last_week_conve)/last_week_conve
                print(rate)
                if rate>0.05:
                    conve_str = "转化率上升了%.2f%%以上"%(rate*100)
        if conve_str:
            result_str_list.append(conve_str)
    else:  #下降
        result_str_list.append('销量比较上周下降')
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
            deal_str.append("上周上了today_deal，今天没有上today_deal")
            if not today_deal_index and has_competitor and deal_index_list[4]:
                deal_str.append("本商品没有上deal,竞品上了deal")
            deal_str = ','.join(deal_str)
            if deal_str:
                result_str_list.append(deal_str)
        # 价格与上周相比是否加价了，如果有竞品，竞品是否降价了
        prices = product_info[0]
        today_price = prices[1]
        last_week_price = prices[3]
        price_str = []
        if today_price and last_week_price and today_price > last_week_price:
            price_str.append("价格与上周相比上升了")
        if has_competitor:
            competitor_today_price = prices[4]
            competitor_last_week_price = prices[6]
            if competitor_today_price and competitor_last_week_price and competitor_today_price < competitor_last_week_price:
                price_str.append("竞品价格下降了")

        price_str = ','.join(price_str)
        if price_str:
                result_str_list.append(price_str)
        # 评分是否下降了，如果有竞品，竞品的评分是否上升了
        review_avg_score = product_info[1]
        today_score = review_avg_score[1]
        last_week_score = review_avg_score[3]
        score_str = []
        if today_score and last_week_score and today_score < last_week_score:
            score_str.append("本商品评分下降了")
        if has_competitor:
            competitor_today_score = review_avg_score[4]
            competitor_last_week_score = review_avg_score[6]
            if competitor_today_score and competitor_last_week_score and competitor_today_score > competitor_last_week_score:
                score_str.append("竞品评分升高了")
        score_str = ','.join(score_str)
        if score_str:
            result_str_list.append(score_str)

        # buybox （今天-上周）/上周<-5%
        buyboxs = product_info[5]
        today_buybox = buyboxs[1]
        last_week_buybox = buyboxs[3]
        buybox_str = ""
        if today_buybox and last_week_buybox:
            today_buybox = float(today_buybox[:-1])
            last_week_buybox = float(last_week_buybox[:-1])
            if last_week_buybox != 0:
                rate = (today_buybox - last_week_buybox) / last_week_buybox
                if rate < -0.05:
                    buybox_str = "buybox上升了%.2f%%以上" % abs(rate * 100)
        if buybox_str:
            result_str_list.append(buybox_str)
        # 转化率 （今天-上周）/上周<-5%

        conve_rates = product_info[4]
        today_conve = conve_rates[1]
        last_week_conve = conve_rates[3]
        conve_str = ''
        if today_conve and last_week_conve:
            today_conve = float(today_conve[:-1])
            last_week_conve = float(last_week_conve[:-1])
            if last_week_conve != 0:
                rate = (today_conve - last_week_conve) / last_week_conve
                if rate < -0.05:
                    conve_str = "转化率下降了%.2f%%以上" % abs(rate * 100)
        if conve_str:
            result_str_list.append(conve_str)

    return result_str_list