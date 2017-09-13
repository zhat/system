from django.shortcuts import render
from .models import StatisticsData,StatisticsOfPlatform
# Create your views here.

def index(request):
    so=StatisticsOfPlatform.objects.all()[:22]
    date_list = []
    data_list = []
    for s in so:
        date_list.append(s.date.strftime("%Y/%m/%d"))
        data_list.append(float(s.dollar_price))
    date_list.reverse()
    data_list.reverse()
    data_list=data_list*2
    date_list=(date_list*2)[:37]
    return render(request,'report/index.html',{'date_list':date_list,'data_list':data_list})