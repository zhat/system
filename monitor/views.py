from django.shortcuts import render
from .models import Station,Feedback
from datetime import datetime,timedelta
import pandas as pd
# Create your views here.
def feedback(request):
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d")
    feedback_count_list = Feedback.objects.filter(date=now_str)
    last_30_days = now - timedelta(days=30)
    last_30_days_str = last_30_days.strftime("%Y-%m-%d")
    days = pd.date_range(start=last_30_days_str, end=now_str)

    date_list = [date.strftime("%Y/%m/%d") for date in days]
    last_week_list = []
    lifetime_list = []
    store_list = ['store1','store2','store3','store4']
    for store in store_list:
        feedback_list = Feedback.objects.filter(date__range=(last_30_days_str, now_str)).filter(store=store)
        last_week = [feedback.last_week for feedback in feedback_list]
        lifetime = [feedback.lifetime for feedback in feedback_list]
        last_week_list.append({'store':store,'last_week':last_week})
        lifetime_list.append({'store':store,'lifetime':lifetime})

    return render(request,"monitor/feedback.html",{'feedback_count_list':feedback_count_list,
                                                   'date_list':date_list,'last_week_list':last_week_list,
                                                   'lifetime_list':lifetime_list,'store_list':store_list})
