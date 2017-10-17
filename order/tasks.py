import time
from celery import shared_task
from datetime import datetime,timedelta
import pymysql
from .get_profile_of_order import get_profile,AmazonOrderManagerCrawlFromOrderId
from django.conf import settings
from .models import OrderData

DATABASE = settings.TASKS_DATABASE

@shared_task
def synchronous_data():
    try:
        dbconn = pymysql.connect(**DATABASE)
        cur = dbconn.cursor()
        sqlcmd = r'INSERT INTO order_orderdata (`profile`,zone,order_id,order_time,`status`) ' \
              r'SELECT DISTINCT a.`profile`,b.platform,b.order_id,b.purchase_at,b.`status` ' \
              r'FROM `amazon_order` b LEFT JOIN `amazon_order_search_data` a ON a.order_id = b.order_id ' \
              r'WHERE b.id > (SELECT amazon_order_id from	order_amazonorder ' \
              r'where id=(SELECT max(id) FROM order_amazonorder));'
        effect_row = cur.execute(sqlcmd)
        print(effect_row)
        print(datetime.now())

        sqlcmd = r'INSERT INTO order_amazonorder (amazon_order_id,zone,order_id,order_time,`status`) ' \
              r'SELECT id,platform,order_id,purchase_at,`status` FROM amazon_order ' \
              r'WHERE order_id =(SELECT order_id from order_orderdata where id = (SELECT max(id) FROM order_orderdata));'
        effect_row = cur.execute(sqlcmd)
        print(effect_row)
        print(datetime.now())
        dbconn.commit()

        sqlcmd = r'UPDATE order_orderdata SET `status`="Shipped" WHERE `status`!="Shipped" ' \
              r'AND id in (SELECT id FROM amazon_order WHERE `status`="Shipped");'

        effect_row = cur.execute(sqlcmd)
        print(effect_row)
        print(datetime.now())
        dbconn.commit()

        sqlcmd = r'UPDATE order_orderdata SET `status`="Canceled" WHERE `status`!="Canceled" ' \
              r'AND id in (SELECT id FROM amazon_order WHERE `status`="Canceled");'

        effect_row = cur.execute(sqlcmd)
        print(effect_row)
        print(datetime.now())
        dbconn.commit()
        return True

        sqlcmd = r'UPDATE order_orderdata SET `status`="Pending" WHERE `status`!="Pending" ' \
              r'AND id in (SELECT id FROM amazon_order WHERE `status`="Pending");'

        effect_row = cur.execute(sqlcmd)
        print(effect_row)
        print(datetime.now())
        dbconn.commit()
    finally:
        cur.close()
        dbconn.close()
    return True

@shared_task
def get_profile_of_order():
    print(datetime.now())
    get_profile('DE', 0)
    get_profile('US', 0)
    get_profile('CA', 0)
    get_profile('JP', 0)
    get_profile('DE', 0, 'Pending')
    get_profile('US', 0, 'Pending')
    get_profile('CA', 0, 'Pending')
    get_profile('JP', 0, 'Pending')
    return True

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i+n]

@shared_task
def get_order_with_asin(asin, profile, zone):
    # 先判断profile是否有对应的orderid
    # 从amazon_order_item查出order_id
    # 判断order_id_list 中是否有
    if OrderData.objects.filter(profile=profile):
        return True
    sqlcmd = r'SELECT order_id FROM order_orderdata WHERE `profile` IS NULL AND zone = "%s" ' \
    r'AND order_id IN (SELECT ao.order_id FROM `amazon_order_item` aot ' \
    r'JOIN `amazon_order` ao ON aot.parent_id = ao.id ' \
    r'WHERE aot.ASIN = "%s");'%(zone,asin)
    print(sqlcmd)
    dbconn = pymysql.connect(**DATABASE)
    cur = dbconn.cursor()
    effect_row = cur.execute(sqlcmd)
    order_id_list = cur.fetchall()
    order_id_list = [x for j in order_id_list for x in j]
    amzCrawl = AmazonOrderManagerCrawlFromOrderId(zone,200)
    for order_list in chunks(order_id_list,300):
        print(order_list)
        amzCrawl.getOrderInfo(order_list)