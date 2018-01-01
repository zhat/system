from selenium import webdriver
import urllib.request
import urllib
import os
from urllib.parse import urlunparse,urlparse,urlencode
import urllib.error
import time
import json
from datetime import datetime,timedelta
import pytesseract
from PIL import Image
from django.conf import settings
from .models import StatisticsData,ReportData,StatisticsOfPlatform,ProductStock,AmazonOrderItem,ProductInfo
#from shibie import GetImageDate

#USER_DATA_DIR = settings.CHROME_USER_DATA_DIR
BASE_URL = "http://192.168.2.99:9080/ocs/index"

def img_to_str(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text.replace(' ','')

class GetStatisticsDataFromOMS():
    """
    从OMS系统上抓取每天统计信息
    """
    def __init__(self):
        self.driver = webdriver.PhantomJS()
    def __del__(self):
        self.driver.quit()
    def get_data_all(self,date):
        zone_info = [
        ('US','US','Amazon.com'),
        ('UK','DE','Amazon.co.uk'),
        ('DE','DE','Amazon.de'),
        ('JP','JP','Amazon.co.jp'),
        ('CA','CA','Amazon.ca'),
        ('ES','DE','Amazon.es'),
        ('IT','DE','Amazon.it'),
        ('FR','DE','Amazon.fr'),
        ]
        for zone,platform,station in zone_info:
            self.get_data(date=date,zone=zone,platform=platform,station=station)
    def get_data(self,date,zone = "US",platform = "US",station = "Amazon.com"):
        """
        :param driver: webdriver.Chrome
        :return:email or ""
        """
        if not isinstance(self.driver,webdriver.PhantomJS):
            raise TypeError
        #time.sleep(5)
        cookie = self.driver.get_cookies()
        cookie = [item["name"] + "=" + item["value"] for item in cookie]
        cookiestr = ';'.join(item for item in cookie)
        current_url = self.driver.current_url
        url_parse = urlparse(current_url)
        host = url_parse.netloc
        origin = urlunparse(url_parse[:2]+('',)*4)
        page = 1
        short_url = urlunparse(url_parse[:3] + ('',) * 3)

        #target_url = "http://192.168.2.99:9080/ocs/salesStatistics/findAll"
        target_url = "http://192.168.2.99:9080/ocs/orderQuery/findAll"
        user_agent = r'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 r'Chrome/60.0.3112.113 Safari/537.36'
        headers = {'cookie':cookiestr,
                'User-Agent':user_agent,
                'Referer':"http://192.168.2.99:9080/ocs/salesStatistics/tolist",
                'Host':host,
                'Origin':origin,
                'X-Requested-With':'XMLHttpRequest',
               }
        querysetlist = []
        while True:
            values = {'param[source]': 'amazon',
                      'param[sku]': '',
                      'param[platform]': platform,
                      'param[status]': '',
                      'param[whichTime]': 'purchaseat',
                      'param[starttime]': date,
                      'param[endtime]': date,
                      'param[timeQuantum]': 0,
                      'param[asin]': '',
                      'param[station]': station,
                      'page': page,
                      'rows': 50}
            data = urlencode(values).encode()
            req = urllib.request.Request(target_url, data=data, headers=headers)
            try:
                result = urllib.request.urlopen(req).read()
            except urllib.error.HTTPError as e:
                print(e)
                return ""
            result = json.loads(result.decode('utf-8'))
            #print(result)
            self.total = result['total']
            self.source = result['source']
            footer = result['footer']
            count_data = footer[1]
            rows = result['rows']
            print(self.total)
            print(self.source)
            now = datetime.now()
            for row in rows:
                data_dict = {'date': date,
                 'sku': row['sku'],
                 'asin': row['asin'],
                 'platform': zone,
                 'station': row['station'],
                 'qty': row['qty'],
                 'currencycode': row['currencycode'],
                 'deduction': row['deduction'],
                 'price': row['price'],
                 'count': row['count'],
                 'sametermrate': row['sametermrate'],
                 'weekrate': row['weekrate'],
                 'monthrate': row['monthrate'],
                 'status': row['status'],
                 'create_date': now,
                 'update_date': now
                 }
                querysetlist.append(StatisticsData(**data_dict))
            if self.total<page*50:
                try:
                    zone_data = {'date':date,'platform':zone,'station':count_data['currencycode'],'qty':count_data['deduction'],
                     'count':count_data['taxrate'],'site_price':float(count_data['weekrate']),
                     'dollar_price':float(count_data['monthrate']),'RMB_price':float(count_data['status']),
                     'create_date':now,'update_date':now}
                except Exception as e:
                    zone_data = {'date':date,'platform':zone,'station':count_data['deduction'],
                     'qty':count_data['taxrate'],'count':count_data['price'],
                     'site_price':float(count_data['weekrate']),'dollar_price':float(count_data['monthrate']),
                     'RMB_price':float(count_data['status']),'create_date':now,'update_date':now}
                StatisticsOfPlatform.objects.create(**zone_data)
                break
            else:
                page+=1
        StatisticsData.objects.bulk_create(querysetlist)

        return result

    def login(self):
        try:
            self.driver.maximize_window()
        except Exception as err:
            print(err)
        frequency = 0
        self.driver.get(BASE_URL)
        while True:
            base_path = settings.IMAGE_PATH
            time_str=int(time.time()*10000000)
            image_path = os.path.join(base_path,"base{}.png".format(time_str))
            image_path_png = os.path.join(base_path,"{}.png".format(time_str))
            self.driver.get_screenshot_as_file(image_path)  # 比较好理解
            im = Image.open(image_path)
            #box = (1022, 360, 1097, 380)  # 设置要裁剪的区域
            box = (745,356,821,380)
            region = im.crop(box)
            region.save(image_path_png)
            username = self.driver.find_element_by_id("username")
            password = self.driver.find_element_by_id("password")
            username.clear()
            username.send_keys(settings.LE_USERNAME)
            #username.send_keys("yaoxuzhao")
            password.clear()
            password.send_keys(settings.LE_PASSWORD)
            #password.send_keys("123")
            val_code = self.driver.find_element_by_id("valCode")
            val_code.clear()
            img_code = img_to_str(image_path_png)
            if not img_code:
                img_code = "abcd"
            val_code.send_keys(img_code)
            time.sleep(3)
            self.driver.find_element_by_xpath("//input[@type='submit']").click()
            time.sleep(5)
            if self.driver.find_elements_by_class_name("header_img"):
                break
            frequency+=1
            if frequency>10:
                raise TimeoutError

    def get_route(self,date):
        """
        计算单品同比和周环比
        """
        # sametermrate
        # weekrate
        rd_list = ReportData.objects.filter(date=date)
        for rd in rd_list:
            yesteerday = rd.date - timedelta(days=1)
            seven_days_ago = rd.date - timedelta(days=7)
            yesteerday_rd = ReportData.objects.filter(date=yesteerday).filter(asin=rd.asin)
            if yesteerday_rd and yesteerday_rd[0].price:
                rd.sametermrate = round((rd.price - yesteerday_rd[0].price) / yesteerday_rd[0].price, 4)
            else:
                rd.sametermrate = 1
            seven_days_ago_rd = ReportData.objects.filter(date=seven_days_ago).filter(asin=rd.asin)
            if seven_days_ago_rd and seven_days_ago_rd[0].price:
                rd.weekrate = round((rd.price - seven_days_ago_rd[0].price) / seven_days_ago_rd[0].price, 4)
            else:
                rd.weekrate = 1
            rd.save()

    def get_sum_route(self,date):
        """
        计算站点的周比和同比
        dollar_price
        sametermrate
        weekrate
        :return:
        """
        sp_list = StatisticsOfPlatform.objects.filter(date=date)
        for sp in sp_list:
            yesteerday = sp.date - timedelta(days=1)
            seven_days_ago = sp.date - timedelta(days=7)
            yesteerday_sp = StatisticsOfPlatform.objects.filter(date=yesteerday)
            if yesteerday_sp and yesteerday_sp[0].dollar_price:
                sp.sametermrate = round(
                    (sp.dollar_price - yesteerday_sp[0].dollar_price) / yesteerday_sp[0].dollar_price, 4)
            else:
                sp.sametermrate = 0
            seven_days_ago_sp = StatisticsOfPlatform.objects.filter(date=seven_days_ago)
            if seven_days_ago_sp and seven_days_ago_sp[0].dollar_price:
                sp.weekrate = round(
                    (sp.dollar_price - seven_days_ago_sp[0].dollar_price) / seven_days_ago_sp[0].dollar_price, 4)
            else:
                sp.weekrate = 0

            sp.save()

def get_data(date):

    time.sleep(6)
    gs = GetStatisticsDataFromOMS()
    gs.login()
    print("Login Success")
    gs.get_data_all(date)

if __name__=="__main__":
    now = datetime.now()
    days = 2
    while days<3:
        date = now-timedelta(days=days)
        date = date.strftime("%Y-%m-%d")
        get_data(date)