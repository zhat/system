from django.shortcuts import render
from django.db.models import Count
from .models import FeedbackInfo, AmazonRefShopList, AmazonProductReviews
from datetime import datetime, timedelta
import pandas as pd
import logging
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import csv
import xlwt
import pandas as pd
# Create your views here.
logger = logging.getLogger('django')


def the_1st_of_the_month(number=12):
    now = datetime.now()
    i = 0
    while True:
        yield now.replace(day=1)
        i += 1
        if i == number:
            break
        now = now.replace(day=1) - timedelta(days=1)


def get_data(date_list, shop_name_list, zone, field):
    tuples = [(shop_name, date)
              for shop_name in shop_name_list for date in date_list]
    index = pd.MultiIndex.from_tuples(tuples, names=['shop_name', 'day'])
    data_frame = pd.DataFrame(0, index=index, columns=[field])
    field_data_list = []
    feedback_list = FeedbackInfo.objects.filter(
        zone=zone).filter(date__in=date_list)
    logger.info(feedback_list)
    for feedback in feedback_list:
        feedback = feedback.to_dict()
        if feedback[field]:
            data_frame.loc[(feedback['shop_name'], feedback['date'].strftime("%Y-%m-%d")), field] = int(
                feedback[field])
        else:
            data_frame.loc[(feedback['shop_name'],
                            feedback['date'].strftime("%Y-%m-%d")), field] = 0
    for shop_name in shop_name_list:
        field_data_list.append({'shop_name': shop_name, field: list(
            map(int, data_frame.loc[shop_name][field].values))})
    max_value = max(list(map(int, data_frame[field].values)))
    interval = pow(10, len(str(max_value)) - 1)
    max_value = (max_value // interval + 1) * interval
    if max_value == 1:
        max_value = 100
    interval = max_value // 10
    return max_value, interval, field_data_list


def feedback(request):
    zone = request.GET.get("zone", '').strip()
    print(zone)
    if not zone:
        zone = 'US'
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    # 站点列表
    zone_list = AmazonRefShopList.objects.filter(
        type="feedback").values("zone").distinct().all()
    zone_list = [zone['zone'] for zone in zone_list]

    # 店铺名称和店铺url
    shop_list = AmazonRefShopList.objects.filter(
        zone=zone).filter(type="feedback")
    shop_name_list = [shop.shop_name for shop in shop_list]
    shop_url_dict = dict((shop.shop_name, shop.shop_url) for shop in shop_list)

    # 当天的各站点数据表格显示
    feedback_table_data = []
    feedback_count_list = FeedbackInfo.objects.filter(
        date=today_str).filter(zone=zone)
    for feedback_count in feedback_count_list:
        feedback_table_data.append({
            'date': feedback_count.date,
            'shop_name': feedback_count.shop_name,
            'shop_url': shop_url_dict[feedback_count.shop_name],
            'last_30_days': feedback_count.last_30_days,
            'last_90_days': feedback_count.last_90_days,
            'last_12_months': feedback_count.last_12_months,
            'lifetime': feedback_count.lifetime,
            'last_week': feedback_count.last_week,
            'last_month': feedback_count.last_month,
            'zone': feedback_count.zone,
        })

    # print(feedback_count_list)
    # 周增量 30个 显示周一数据  周增量=当前天数据减周一数据  如果当前为周一 则减上周一数据
    # 如果今天为周一 则显示30个周一的数据  如果今天不是周一 则显示29个周一数据和当前的数据
    # weekday 周一 0 周二 1  周三 2 周四 3 周五 4 周六 5 周日 6
    # 如果now.weekday()为0 表示当天为周一 最近的周一为当天  如果不为0 则减去相应天数 得到本周一的日期
    last_monday = now - timedelta(days=now.weekday()) if now.weekday() else now
    last_monday_str = last_monday.strftime("%Y-%m-%d")
    # 30个周一
    start_monday = last_monday - timedelta(days=7 * 30)
    start_monday_str = start_monday.strftime("%Y-%m-%d")

    days = pd.date_range(start=start_monday_str,
                         end=last_monday_str, freq="7D")
    week_date_list = [(date - timedelta(days=1)).strftime("%Y-%m-%d")
                      for date in days]  # 日期列表
    list_week_date_list = [date.strftime("%Y-%m-%d") for date in days]  # 日期列表
    if now.weekday():  # 今天不是星期一 去掉第一个周一 加上今天的日期
        week_date_list.pop(0)
        week_date_list.append(now.strftime("%Y-%m-%d"))
        list_week_date_list.pop(0)
        list_week_date_list.append(now.strftime("%Y-%m-%d"))

    # get_data(date_list,shop_name_list,zone,field):
    max_value_of_weeks, interval_of_weeks, last_week_list = get_data(list_week_date_list,
                                                                     shop_name_list, zone, "last_week")
    # 最近12个月的月增量
    dates = [date for date in the_1st_of_the_month()]
    months = [(date - timedelta(days=1)).strftime("%Y-%m")
              for date in dates]  # 每月1号的数据是上个月的统计
    months.reverse()
    the_month_date_list = [date.strftime("%Y-%m-%d") for date in dates]
    the_month_date_list.reverse()
    if now.day != 1:
        months.pop(0)
        months.append(now.strftime("%Y-%m"))
        the_month_date_list.pop(0)
        the_month_date_list.append(now.strftime("%Y-%m-%d"))

    max_value_of_months, interval_of_months, last_month_list = get_data(the_month_date_list,
                                                                        shop_name_list, zone, "last_month")

    return render(request, "monitor/feedback.html", {'feedback_count_list': feedback_table_data,  # table数据
                                                     'shop_name_list': shop_name_list,  # 店铺列表
                                                     'list_week_date_list': week_date_list,  # 周增量日期
                                                     'max_value_of_weeks': max_value_of_weeks,  # 周增量最大值
                                                     'interval_of_weeks': interval_of_weeks,  # 周增量间隔
                                                     'last_week_list': last_week_list,  # 周增量数据
                                                     'months': months,  # 月增量月份
                                                     'max_value_of_months': max_value_of_months,  # 月增量最大值
                                                     'interval_of_months': interval_of_months,  # 月增量间隔
                                                     'last_month_list': last_month_list,  # 月增量数据
                                                     'zones': zone_list,'zone':zone})


def feedback_week(request):
    zone = request.GET.get("zone", '').strip()
    print(zone)
    if not zone:
        zone = 'US'
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    # 站点列表
    zone_list = AmazonRefShopList.objects.filter(
        type="feedback").values("zone").distinct().all()
    zone_list = [zone['zone'] for zone in zone_list]

    # 店铺名称和店铺url
    shop_list = AmazonRefShopList.objects.filter(
        zone=zone).filter(type="feedback")
    shop_name_list = [shop.shop_name for shop in shop_list]
    shop_url_dict = dict((shop.shop_name, shop.shop_url) for shop in shop_list)

    # print(feedback_count_list)
    # 周增量 30个 显示周一数据  周增量=当前天数据减周一数据  如果当前为周一 则减上周一数据
    # 如果今天为周一 则显示30个周一的数据  如果今天不是周一 则显示29个周一数据和当前的数据
    # weekday 周一 0 周二 1  周三 2 周四 3 周五 4 周六 5 周日 6
    # 如果now.weekday()为0 表示当天为周一 最近的周一为当天  如果不为0 则减去相应天数 得到本周一的日期
    last_monday = now - timedelta(days=now.weekday()) if now.weekday() else now
    last_monday_str = last_monday.strftime("%Y-%m-%d")
    # 30个周一
    start_monday = last_monday - timedelta(days=7 * 30)
    start_monday_str = start_monday.strftime("%Y-%m-%d")

    days = pd.date_range(start=start_monday_str,
                         end=last_monday_str, freq="7D")
    week_date_list = [(date - timedelta(days=1)).strftime("%Y-%m-%d")
                      for date in days]  # 日期列表
    list_week_date_list = [date.strftime("%Y-%m-%d") for date in days]  # 日期列表
    if now.weekday():  # 今天不是星期一 去掉第一个周一 加上今天的日期
        week_date_list.pop(0)
        week_date_list.append(now.strftime("%Y-%m-%d"))
        list_week_date_list.pop(0)
        list_week_date_list.append(now.strftime("%Y-%m-%d"))

    # get_data(date_list,shop_name_list,zone,field):
    max_value_of_weeks, interval_of_weeks, last_week_list = get_data(list_week_date_list,
                                                                     shop_name_list, zone, "last_week")

    return render(request, "monitor/feedback_week_line.html", {
        'shop_name_list': shop_name_list,  # 店铺列表
        'list_week_date_list': week_date_list,  # 周增量日期
        'max_value_of_weeks': max_value_of_weeks,  # 周增量最大值
        'interval_of_weeks': interval_of_weeks,  # 周增量间隔
        'last_week_list': last_week_list,  # 周增量数据
        'zones': zone_list})


def review_add_day(request):
    date = request.GET.get("date","").strip()
    zone = "US"
    if not date:
        now = datetime.now()
        date = (now-timedelta(days=1)).strftime("%Y-%m-%d")

def review_counts(request):
    date = request.GET.get("date", '').strip()
    zone = "US"
    if not date:
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
    start = datetime.strptime(date,"%Y-%m-%d")
    """objects.values('authors__name').annotate(Sum('price'))"""
    reviews = AmazonProductReviews.objects.using('front').values('asin').\
        filter(review_date=start).annotate(count=Count('id')).order_by('-count')
    print(reviews)
    return render(request, "monitor/review_of_asin.html", {"zone":zone, "date":date, "reviews":reviews})

def review_count_with_asin(request):
    asin = request.GET.get("asin", '').strip()
    if not asin:
        asin = "B005FEGYJC"
    zone = "US"
    """objects.values('authors__name').annotate(Sum('price'))"""
    """ordering = 'CASE WHEN shop_name="NEON MART" THEN 1 ELSE 2 END'
        feedback_count_list = FeedbackInfo.objects.filter(date=now_str).filter(zone=zone).extra(
           select={'ordering': ordering}, order_by=('ordering','shop_name'))"""
    date_format = r'DATE_FORMAT(create_date,"%%Y-%%m-%%d")'
    reviews = AmazonRefShopList.objects.using('front').extra(select={'date':date_format}).values('date').\
        filter(asin=asin).annotate(count=Count('id')).order_by('date')
    print(reviews.query)
    return render(request, "monitor/review_of_asin_detail.html", {"zone":zone, "asin":asin, "reviews":reviews})

def review_detail(request):
    asin = "B005FEGYJC"
    AmazonProductReviews.objects.using('front').filter(asin=asin).filter()


def review_of_zone(request):
    date = request.GET.get("date", '').strip()
    if not date:
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
    start = datetime.strptime(date, "%Y-%m-%d")
    """objects.values('authors__name').annotate(Sum('price'))"""
    reviews = AmazonProductReviews.objects.using('front').values('zone').\
        annotate(count=Count('id')).order_by('-count')
    # print(reviews)
    return render(request, "monitor/review_of_zone.html", {"reviews": reviews})

def review_of_asin(request):
    date = request.GET.get("date", '').strip()
    zone = request.GET.get("zone","US").strip()
    if not zone:
        zone = "US"
    if not date:
        now = datetime.now()
        date = (now-timedelta(days=1)).strftime("%Y-%m-%d")
    start = datetime.strptime(date,"%Y-%m-%d")
    """objects.values('authors__name').annotate(Sum('price'))"""
    reviews = AmazonProductReviews.objects.using('front').values('asin').filter(zone=zone).\
        annotate(count=Count('id')).order_by('-count')
    paginator = Paginator(reviews, 20)  # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        review_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page = 1
        review_list = paginator.page(page)
    zones = ["US","DE","UK","CA","FR","IT","ES","JP"]
    return render(request,"monitor/review_of_asin.html",{"zone":zone,"zones":zones,"start_index":(int(page)-1)*10,
                                                         "date":date,"reviews":review_list})

def review_of_asin_detail(request):
    zone = request.GET.get("zone","").strip()
    asin = request.GET.get("asin", '').strip()
    star_str = request.GET.get("star", '').strip()
    start = request.GET.get("start", '').strip()
    end = request.GET.get("end", '').strip()

    if not zone:
        zone = "US"
    """objects.values('authors__name').annotate(Sum('price'))
    reviews = AmazonProductReviews.objects.using('front').values('review_star').filter(zone=zone).filter(asin=asin). \
        annotate(count=Count('id')).order_by('-review_star')
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    count5 = 0
    for review in reviews:
        if review["review_star"] == "5.0":
            count5 = review['count']
        elif review["review_star"] == "4.0":
            count4 = review['count']
        elif review["review_star"] == "3.0":
            count3 = review['count']
        elif review["review_star"] == "2.0":
            count2 = review['count']
        elif review["review_star"] == "1.0":
            count1 = review['count']
    count_all = AmazonProductReviews.objects.using('front').values('id').filter(zone=zone).filter(asin=asin).count()
    #print(reviews)
    count = count1+count2+count3+count4+count5
    #print(count,count_all)
    reviews = {
        'asin': asin,
        'count_all': count_all,
        'count1': count1,
        'count2': count2,
        'count3': count3,
        'count4': count4,
        'count5': count5,
    }"""
    review_detail_list = AmazonProductReviews.objects.using('front').filter(zone=zone)
    if asin:
        review_detail_list = review_detail_list.filter(asin=asin)
    if star_str:
        print(star_str)
        star_list = star_str.split("_")
        star_list = [star+".0" for star in star_list]
        review_detail_list = review_detail_list.filter(review_star__in=star_list)
    if start:
        review_detail_list = review_detail_list.filter(review_date__gte=start)
    if end:
        review_detail_list = review_detail_list.filter(review_date__lte=end)
    review_detail_list = review_detail_list.order_by("-review_date")
    result_count = review_detail_list.count()
    paginator = Paginator(review_detail_list, 10)  # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        review_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page = 1
        review_list = paginator.page(page)

    zone_url = zone_to_domain(zone)

    return render(request, "monitor/review_of_asin_detail.html", {"star":star_str,"result_count":result_count,
                                                                  "zone": zone,"asin":asin,
                                                                  "start":start,"end":end,
                                                                  "start_index":(int(page)-1)*10,
                                                                  "zone_url":zone_url,
                                                                  "review_list":review_list})

def review_to_csv(request):
    zone = request.GET.get("zone","").strip()
    asin = request.GET.get("asin", '').strip()
    star_str = request.GET.get("star", '').strip()
    start = request.GET.get("start", '').strip()
    end = request.GET.get("end", '').strip()

    if not zone:
        zone = "US"
    """objects.values('authors__name').annotate(Sum('price'))"""
    review_detail_list = AmazonProductReviews.objects.using('front').filter(zone=zone,asin=asin)
    if star_str:
        print(star_str)
        star_list = star_str.split("_")
        star_list = [star+".0" for star in star_list]
        review_detail_list = review_detail_list.filter(review_star__in=star_list)
    if start:
        review_detail_list = review_detail_list.filter(review_date__gte=start)
    if end:
        review_detail_list = review_detail_list.filter(review_date__lte=end)
    review_detail_list = review_detail_list.order_by("-review_date")

    zone_url = zone_to_domain(zone)
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('test', cell_overwrite_ok=True)
    for review in review_detail_list:
        pass
    sheet.write(0, 0, 'EnglishName')  # 其中的'0-行, 0-列'指定表中的单元，'EnglishName'是向该单元写入的内容
    sheet.write(1, 0, 'Marcovaldo')
    txt1 = '中文名字'
    sheet.write(0, 1, txt1)  # 此处需要将中文字符串解码成unicode码，否则会报错
    txt2 = '马可瓦多'
    sheet.write(1, 1, txt2)

    # 最后，将以上操作保存到指定的Excel文件中
    book.save(r'e:\test1.xls')  # 在字符串前加r，声明为raw字符串，这样就不会处理其中的转义了。否则，可能会报错
    writer = pd.ExcelWriter('output.xlsx')
    df1 = pd.DataFrame(data={'col1': [1, 1], 'col2': [2, 2]})
    df1.to_excel(writer, 'Sheet1')
    writer.save()
    with open("test.csv", "w",encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # 先写入columns_name
        # "序号	zone	asin	标题	评论内容	用户	评分	评论日期"
        writer.writerow(["zone", "asin","标题","评论内容","用户","评分","评论日期"])
        # 写入多行用writerows
        for review in review_detail_list:
            writer.writerow([review.zone,review.asin,review.review_title,review.review_text,review.reviewer_name,
                             review.review_star,review.review_date])

    return render(request, "monitor/review_of_asin_detail.html", {"star":star_str,
                                                                  "zone": zone,"asin":asin,
                                                                  "start":start,"end":end,"zone_url":zone_url})


def zone_to_domain(zone):
    switcher = {
            'US': 'https://www.amazon.com',
            'UK': 'https://www.amazon.co.uk',
            'DE': 'https://www.amazon.de',
            'JP': 'https://www.amazon.jp',
            'CA': 'https://www.amazon.ca',
            'ES': 'https://www.amazon.es',
            'IT': 'https://www.amazon.it',
            'FR': 'https://www.amazon.fr',
    }

    return switcher.get(zone, 'https://www.amazon.com')