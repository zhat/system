# coding = utf-8
from datetime import datetime
import pandas as pd
import pymysql

"""
    模拟登录下载订单管理页面数据
"""

# for example
# /merchant-picker/change-merchant?url=%2F&marketplaceId=A1F83G8C2ARO7P&merchantId=AV7KSH7XB8RNM
# '/merchant-picker/change-merchant?url=%2F&marketplaceId=' + marketplaceid_dict[zone] + '&merchantId=' +  merchantId_dict[zone]
# change key and value
# url = 'https://sellercentral.amazon.es/gp/homepage.html?'

def data_from_db():
    dbconn = pymysql.connect(
            host="192.168.2.97",
            database="bi_system",
            user="lepython",
            password="qaz123456",
            port=3306,
            charset='utf8'
        )
    cur = dbconn.cursor()

    get_max_id = r'SELECT max(id) FROM order_orderdata;'
    cur.execute(get_max_id)
    result = cur.fetchall()
    print(result)

    sqlcmd = r'INSERT INTO order_orderdata (id,profile,zone,order_id,order_time) ' \
             r'SELECT DISTINCT b.id,a.profile,b.platform,b.order_id,b.purchase_at ' \
             r'FROM `amazon_order` b LEFT JOIN `amazon_order_search_data` a ON a.order_id = b.order_id ' \
             r'WHERE b.id>%d;'%result[0][0]
    print(sqlcmd)
    cur.execute(sqlcmd)
    dbconn.commit()
    result = cur.fetchall()
    print(result)

    sqlcmd = r'update `order_orderdata` a,`amazon_order_search_data` b ' \
    r'set a.`profile` = b.`profile` ' \
    r'where a.order_id = b.order_id ' \
    r'and a.`profile` is NULL;'

    print(sqlcmd)
    cur.execute(sqlcmd)
    dbconn.commit()
    result = cur.fetchall()
    print(result)

    cur.close()
    dbconn.close()

if __name__=='__main__':
    data_from_db()