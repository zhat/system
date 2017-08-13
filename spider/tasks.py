import time
from celery import shared_task
from datetime import datetime
from .AmazonOrdersCrawl.AmazonManagerOrderCrawlFromAsin import AmazonOrderManagerCrawlFromAsin_
from .AmazonOrdersCrawl.AutoUpdateData import  AutoUpdateData
from .models import OrderCrawl

@shared_task
def add(x, y):
    time.sleep(10)
    return x + y

@shared_task
def mul(x, y):
    return x * y
 
@shared_task
def xsum(numbers):
    return sum(numbers)

@shared_task
def get_order_info(id):

    order=OrderCrawl.objects.get(id=id)
    zone=order.zone
    asin=order.asin
    days=order.days
    zone_lower_case = zone.lower()
    order.start_time= datetime.now()
    order.save()
    amzCrawl = AmazonOrderManagerCrawlFromAsin_(zone, asin, '2017-08-02', '2013-01-01', days)  # 每次启动跑16天的数据，截至到当天往前推62天

    amzCrawl.getOrderInfo()
    time.sleep(120)
    executor = AutoUpdateData()
    executor._update_data_by_asin(zone_lower_case)
    executor._exit()
    order.end_time = datetime.now()
    order.save()
    return order.id