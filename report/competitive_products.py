import os
import xlrd
import pymysql
from .models import CompetitiveProduct

TASKS_DATABASE = {
	    'host':"192.168.2.97",
		'database':"bi_system",
		'user':"lepython",
		'password':"qaz123456",
		'port':3306,
		'charset':'utf8'
}
def get_competitive():
    ##从excel文件获取库存
    dbconn = pymysql.connect(**TASKS_DATABASE)
    file_name = "类目平均分统计_20171128.xlsx"
    base_path = "D:/"
    file_path = os.path.join(base_path,file_name)
    print(file_path)
    if os.path.exists(file_path):
        data = xlrd.open_workbook(file_path)

        for table in data.sheets():
            print(table)
            nrows = table.nrows  # 行数
            ncols = table.ncols  # 列数
            print(nrows,ncols)
            for i in range(nrows):
                row_values = table.row_values(i)
                if row_values[0]=="SKU":
                    continue
                elif row_values[0]=="平均评分":
                    break
                else:
                    #print(row_values)
                    sku = row_values[0]
                    score = row_values[1]
                    comments = row_values[2]
                    competitive_product_asin = row_values[3]
                    competitive_product_score = row_values[4]
                    competitive_product_comments = row_values[5]
                    try:
                        comments = int(float(comments))
                    except Exception as e:
                        print(e)
                    try:
                        competitive_product_comments = int(float(competitive_product_comments))
                    except Exception as e:
                        print(e)
                    asin = ""
                    zone = ""
                    try:
                        #如果sku 全是数字 会显示为float类型 会多个.0 所以转成int型
                        sku = int(float(sku))
                    except Exception as e:
                        print(e)
                    sql = r"SELECT DISTINCT b.platform,a.ASIN FROM `amazon_order_item` a JOIN `amazon_order` b " \
                          r"ON a.parent_id=b.id WHERE sku = '{}';".format(sku)
                    cur = dbconn.cursor()
                    cur.execute(sql)
                    result_list = cur.fetchall()
                    for result in result_list:
                        zone = result[0]
                        asin = result[1]
                        competier = CompetitiveProduct.objects.filter(zone=zone).filter(asin=asin).all()
                        if competier:
                            continue
                        info = {'sku': sku, 'score': score, 'comments': comments,'zone':zone,'asin':asin,
                            'competitive_product_asin': competitive_product_asin,
                            'competitive_product_score': competitive_product_score,
                            'competitive_product_comments': competitive_product_comments}
                        new_cp = CompetitiveProduct(**info)
                        new_cp.save()
                        print(info)
    else:
        print("文件不存在")
            #ProductStock.objects.create(date=date_str,sku=sku,stock=stock,quantity=quantity,reserved=reserved,
            #                            platform=platform,station=station)

if __name__ == "__main__":
    get_competitive()