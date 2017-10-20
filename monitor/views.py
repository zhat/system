from django.shortcuts import render
from .models import FeedbackInfo,AmazonRefShopList
from datetime import datetime,timedelta
import pandas as pd
# Create your views here.
def feedback(request):
    zone = request.GET.get("zone",'').strip()
    print(zone)
    if not zone:
        zone='us'
    start = request.GET.get('start', '').strip()
    end = request.GET.get('end', '').strip()
    if start:  # 有开始时间
        start_date = datetime.strptime(start, '%Y-%m-%d')
        if end:
            end_date = start_date + timedelta(days=30)  # 开始时间30天后
            end = datetime.strptime(end, '%Y-%m-%d')
            end = end_date if end_date < end else end
            end = end.strftime("%Y-%m-%d")
        else:
            end_date = datetime.now()
            end = start_date + timedelta(days=30)  # 开始时间30天后
            end = end_date if end_date < end else end  # 两天前和开始时间30天后中的小值
            end = end.strftime("%Y-%m-%d")
    else:  # 没有开始时间
        if end:
            end = datetime.strptime(end, '%Y-%m-%d')
            start = end - timedelta(days=30)
            start = start.strftime("%Y-%m-%d")
            end = end.strftime("%Y-%m-%d")
        else:
            now = datetime.now()
            end = now
            end = end.strftime("%Y-%m-%d")
            start = now - timedelta(days=30)
            start = start.strftime("%Y-%m-%d")
    now = datetime.now()
    zone_list=AmazonRefShopList.objects.filter(type="feedback").values("zone").distinct().all()
    #print(zone_list)
    zones = [zone['zone'] for zone in zone_list]
    #print(zones)
    shop_list = AmazonRefShopList.objects.filter(zone=zone).filter(type="feedback")
    #print(shop_list)
    now_str = now.strftime("%Y-%m-%d")
    feedback_count_list = FeedbackInfo.objects.filter(date=now_str).filter(zone=zone)
    #print(feedback_count_list)
    days = pd.date_range(start=start, end=end)
    #shop_name_list = ['ANKER', 'HYPERIKON', 'TAO TRONICS', 'NEON MART']
    shop_name_list = [shop.shop_name for shop in shop_list]
    shop_url_dict = dict((shop.shop_name,shop.shop_url) for shop in shop_list)
    feedback_table_data=[]
    for feedback_count in feedback_count_list:
        feedback_table_data.append({
            'date':feedback_count.date,
            'shop_name':feedback_count.shop_name,
            'shop_url': shop_url_dict[feedback_count.shop_name],
            'last_30_days': feedback_count.last_30_days,
            'last_90_days': feedback_count.last_90_days,
            'last_12_months': feedback_count.last_12_months,
            'lifetime': feedback_count.lifetime,
            'last_day': feedback_count.last_day,
            'last_week': feedback_count.last_week,
            'zone': feedback_count.zone,
        })
    tuples = [(shop_name,day) for shop_name in shop_name_list for day in days]
    index = pd.MultiIndex.from_tuples(tuples, names=['shop_name','day'])
    data_frame = pd.DataFrame(0,index=index, columns=['last_day','lifetime'])
    date_list = [date.strftime("%Y/%m/%d") for date in days]
    last_day_list = []
    lifetime_list = []
    feedback_list = FeedbackInfo.objects.filter(zone=zone).filter(date__range=(start,end))
    for feedback in feedback_list:
        data_frame.loc[(feedback.shop_name,feedback.date.strftime("%Y-%m-%d")), 'lifetime'] = int(feedback.lifetime)
        print(feedback.last_day)
        if feedback.last_day:
            data_frame.loc[(feedback.shop_name, feedback.date.strftime("%Y-%m-%d")), 'last_day'] = int(feedback.last_day)
        else:
            data_frame.loc[(feedback.shop_name, feedback.date.strftime("%Y-%m-%d")), 'last_day'] = 0
    print(data_frame)
    for shop_name in shop_name_list:
        lifetime = list(map(int,data_frame.loc[shop_name]['lifetime'].values))
        last_day = list(map(int,data_frame.loc[shop_name]['last_day'].values))
        print(lifetime)
        print(last_day)

        last_day_list.append({'shop_name': shop_name, 'last_day': last_day})
        lifetime_list.append({'shop_name': shop_name, 'lifetime': lifetime})
    max_lifetime = (max(list(map(int,data_frame['lifetime'].values))) // 10000 + 1) * 10000
    interval_lifetime = max_lifetime // 10
    max_last_day = (max(list(map(int, data_frame['last_day'].values))) // 100 + 1) * 100
    interval_last_day = max_last_day // 10
    return render(request,"monitor/feedback.html",{'feedback_count_list':feedback_table_data,
                                                   'date_list':date_list,'last_day_list':last_day_list,
                                                   'lifetime_list':lifetime_list,'shop_name_list':shop_name_list,
                                                   'max_lifetime':max_lifetime,'interval_lifetime':interval_lifetime,
                                                   'max_last_day':max_last_day,'interval_last_day':interval_last_day,
                                                   'zones':zones})
