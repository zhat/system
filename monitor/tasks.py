import time
import os
import random
from celery import shared_task
from .models import Station,Feedback
from datetime import datetime,timedelta

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
