from django.shortcuts import render
from .models import FeedbackInfo, AmazonRefShopList
from datetime import datetime, timedelta
import pandas as pd
import logging
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
        zone = 'us'
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
                                                     'zones': zone_list})


def feedback_week(request):
    zone = request.GET.get("zone", '').strip()
    print(zone)
    if not zone:
        zone = 'us'
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
