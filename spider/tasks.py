import time
from celery import shared_task
from datetime import datetime
from .AmazonOrdersCrawl.AmazonManagerOrderCrawlFromAsin import AmazonOrderManagerCrawlFromAsin_
from .AmazonOrdersCrawl.AutoUpdateData import  AutoUpdateData
from .models import OrderCrawl
from .AmazonOrdersCrawl.AmazonManagerOrderCrawlFromOrderID import get_profile

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
    try:
        order=OrderCrawl.objects.get(id=id)
        zone=order.zone
        asin=order.asin
        days=order.days
        zone_lower_case = zone.lower()
        order.start_time= datetime.now()
        order.save()
        amzCrawl = AmazonOrderManagerCrawlFromAsin_(zone, asin, '2017-08-02', '2017-01-01', days)  # 每次启动跑16天的数据，截至到当天往前推62天

        amzCrawl.getOrderInfo()
        executor = AutoUpdateData()
        executor._update_data_by_asin(zone_lower_case)
        executor._exit()
        order.end_time = datetime.now()
        order.save()
    except:
        pass
    return "执行结束"
@shared_task
def get_profile_by_order_id():
    get_profile('JP', 48)
    get_profile('CA', 48)
    get_profile('DE',48)
    get_profile('US', 48)
