import random
from celery import shared_task
from .models import Station,Feedback,FeedbackInfo,AmazonRefShopList
from datetime import datetime,timedelta
from django.core.mail import send_mail
from django.template import loader
from django.conf import settings

@shared_task
def insert_data():
    station = Station.objects.filter(station="amazon.com").first()
    now = datetime.now()
    days = 0
    while days<60:
        date = now - timedelta(days=days)
        date_str = date.strftime("%Y-%m-%d")
        days += 1
        if Feedback.objects.filter(date=date_str):
            continue
        for store in ['store1','store2','store3','store4']:
            Feedback.objects.create(date=date_str,store=store,station=station,last_30_days=500,
                                    last_90_days=1500,last_12_months=6000,lifetime=random.randint(10000,20000),
                                    last_day=20,last_week=random.randint(100,200))

@shared_task
def update_feedback():
    feedback_list = FeedbackInfo.objects.all()
    for feedback in feedback_list:
        if not feedback.last_week:
            start_date = feedback.date
            last_week = start_date-timedelta(days=7)
            last_week_str = last_week.strftime('%Y-%m-%d')
            last_week_feedback = FeedbackInfo.objects.filter(date=last_week_str).\
                filter(zone=feedback.zone).filter(shop_name=feedback.shop_name)
            if last_week_feedback:
                feedback.last_week=feedback.lifetime-last_week_feedback[0].lifetime
        if not feedback.last_day:
            start_date = feedback.date
            last_day = start_date - timedelta(days=1)
            last_day_str = last_day.strftime('%Y-%m-%d')
            last_day_feedback = FeedbackInfo.objects.filter(date=last_day_str). \
                filter(zone=feedback.zone).filter(shop_name=feedback.shop_name)
            if last_day_feedback:
                feedback.last_day = feedback.lifetime - last_day_feedback[0].lifetime
        feedback.save()

@shared_task
def send_email():
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d")
    date_str = now.strftime("%Y%m%d")
    zone_list = AmazonRefShopList.objects.filter(type="feedback").values("zone").distinct().all()
    # print(zone_list)
    zones = [zone['zone'] for zone in zone_list]
    zone_feedback_list =[]
    for zone in zones:
        shop_list = AmazonRefShopList.objects.filter(zone=zone).filter(type="feedback")
        # print(shop_list)
        feedback_count_list = FeedbackInfo.objects.filter(date=now_str).filter(zone=zone)
        shop_name_list = [shop.shop_name for shop in shop_list]
        shop_url_dict = dict((shop.shop_name, shop.shop_url) for shop in shop_list)
        feedback_table_data = []
        for feedback_count in feedback_count_list:
            feedback_table_data.append({
                'date': feedback_count.date.strftime("%Y-%m-%d"),
                'shop_name': feedback_count.shop_name,
                'shop_url': shop_url_dict[feedback_count.shop_name],
                'last_30_days': feedback_count.last_30_days,
                'last_90_days': feedback_count.last_90_days,
                'last_12_months': feedback_count.last_12_months,
                'lifetime': feedback_count.lifetime,
                'last_day': feedback_count.last_day,
                'last_week': feedback_count.last_week,
                'zone': feedback_count.zone,
            })
        zone_feedback_list.append(feedback_table_data)

    email_template_name = '../templates/monitor/email.html'
    t = loader.get_template(email_template_name)
    context={'zone_feedback_list':zone_feedback_list,'date':now_str}
    html_content = t.render(context)
    send_mail('Feedback统计'+date_str,
              '',
              settings.EMAIL_FROM,
              settings.EMAIL_TO,
              html_message=html_content)
    return True