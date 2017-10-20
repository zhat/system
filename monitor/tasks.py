import random
from celery import shared_task
from .models import Station,Feedback,FeedbackInfo
from datetime import datetime,timedelta

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