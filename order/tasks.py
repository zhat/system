import time
from celery import shared_task
from datetime import datetime,timedelta
import pymysql
from .get_profile_of_order import get_profile
from django.conf import settings

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