from selenium import webdriver
import urllib.request
import urllib
import os
from urllib.parse import urlunparse,urlparse,urlencode
import urllib.error
import time
import json
import pymysql
from datetime import datetime,timedelta
import pytesseract
from PIL import Image
from django.conf import settings
#from shibie import GetImageDate

#USER_DATA_DIR = settings.CHROME_USER_DATA_DIR
BASE_URL = "http://192.168.2.99:9080/ocs/index"
DATABASE = settings.TASKS_DATABASE
#DATABASE = {
#            'host':"192.168.2.97",
#            'database':"bi_system_dev",
#            'user':"lepython",
#            'password':"qaz123456",
#            'port':3306,
#            'charset':'utf8'
#}


def img_to_str(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text.replace(' ','')

class GetStatisticsDataFromOMS():
    """
    从OMS系统上抓取每天统计信息
    """
    def __init__(self,date):
        self.dbconn = pymysql.connect(**DATABASE)
        self.date=date
    def get_data(self,driver):
        """
        :param driver: webdriver.Chrome
        :return:email or ""
        """
        if not isinstance(driver,webdriver.PhantomJS):
            raise TypeError
        #time.sleep(5)
        cookie = driver.get_cookies()
        cookie = [item["name"] + "=" + item["value"] for item in cookie]
        cookiestr = ';'.join(item for item in cookie)
        print(cookiestr)
        current_url = driver.current_url
        url_parse = urlparse(current_url)
        host = url_parse.netloc
        origin = urlunparse(url_parse[:2]+('',)*4)
        print(host)
        print(origin)
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

        sql_insert = []
        while True:
            values = {'param[source]': 'amazon',
                      'param[sku]': '',
                      'param[platform]': 'US',
                      'param[status]': '',
                      'param[whichTime]': 'purchaseat',
                      'param[starttime]': self.date,
                      'param[endtime]': self.date,
                      'param[timeQuantum]': 0,
                      'param[asin]': '',
                      'param[station]': 'Amazon.com',
                      'page': page,
                      'rows': 50}
            # values=json.dumps(values)
            #print(values)
            data = urlencode(values).encode()
            # data=b'param%5Bsource%5D=amazon&param%5Bsku%5D=&param%5Bplatform%5D=&param%5Bstatus%5D=&param%5BwhichTime%5D=purchaseat&param%5Bstarttime%5D=&param%5Bendtime%5D=&param%5BtimeQuantum%5D=-30&param%5Basin%5D=&param%5Bstation%5D=&page=1&rows=50'

            #print(data)
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
            for row in rows:
                # print(row['sku'], row['asin'], row['platform'], row['station'], row['qty'], row['currencycode'],
                #   row['deduction'],
                #   row['price'], row['count'], row['sametermrate'], row['weekrate'], row['monthrate'], row['status'])
                insert_url = r'INSERT INTO report_statisticsdata (`date`,sku,asin,platform,station,qty,currencycode,' \
                     r'deduction,price,`count`,sametermrate,weekrate,monthrate,status)' \
                     r' VALUES("%s","%s","%s","%s","%s",%d,"%s",%f,%f,%d,%f,%f,%f,"%s");'%(self.date,
                row['sku'],row['asin'],row['platform'],row['station'],row['qty'],row['currencycode'],row['deduction'],
                row['price'],row['count'],row['sametermrate'],row['weekrate'],row['monthrate'],row['status'])
                #print(insert_url)
                sql_insert.append(insert_url)
            if self.total<page*50:
                # print(self.date,count_data['currencycode'],count_data['deduction'],count_data['taxrate'],
                #       float(count_data['weekrate']),float(count_data['monthrate']),float(count_data['status']),
                #       float(count_data['sametermrate'][:-1]),float(count_data['price'][:-1]),
                #       float(count_data['count'][:-1]))
                print(count_data)
                try:
                    insert_url = r'INSERT INTO report_statisticsofplatform (`date`,station,qty,`count`,' \
                                 r'site_price,dollar_price,RMB_price) ' \
                                 r'VALUES("%s","%s",%d,%d,%f,%f,%f);' % (self.date,
                                                                         count_data['currencycode'],
                                                                         count_data['deduction'],
                                                                         count_data['taxrate'],
                                                                         float(count_data['weekrate']),
                                                                         float(count_data['monthrate']),
                                                                         float(count_data['status']),
                                                                         )
                except Exception as e:
                    print(e)
                    insert_url = r'INSERT INTO report_statisticsofplatform (`date`,station,qty,`count`,' \
                                 r'site_price,dollar_price,RMB_price) ' \
                                 r'VALUES("%s","%s",%d,%d,%f,%f,%f);' % (self.date,
                                                                         count_data['deduction'], count_data['taxrate'],
                                                                         count_data['price'],
                                                                         float(count_data['weekrate']),
                                                                         float(count_data['monthrate']),
                                                                         float(count_data['status']),
                                                                         )
                #print(insert_url)
                sql_insert.append(insert_url)
                break
            else:
                page+=1
        cur = self.dbconn.cursor()

        for sqlcmd in sql_insert:
                #print(sqlcmd)
            cur.execute(sqlcmd)
        print(datetime.now())
        self.dbconn.commit()
        cur.close()
        return result

    def clean_data(self):
        cur = self.dbconn.cursor()
        sqlcmd = r'INSERT INTO report_asininfo(`date`,`asin`,`platform`,station,sku) SELECT DISTINCT ' \
                 r'`date`,`asin`,`platform`,station,sku FROM report_statisticsdata WHERE date="%s";'%self.date

        cur.execute(sqlcmd)
        #print(sqlcmd)
        self.dbconn.commit()
        #except Exception as e:
        #    print(e)
        #finally:
        cur.close()
    def login(self,driver):
        try:
            driver.maximize_window()
        except Exception as err:
            print(err)
        while True:
            base_path = settings.IMAGE_PATH
            time_str=int(time.time()*10000000)
            image_path = os.path.join(base_path,"base{}.png".format(time_str))
            image_path_png = os.path.join(base_path,"{}.png".format(time_str))
            driver.get_screenshot_as_file(image_path)  # 比较好理解
            im = Image.open(image_path)
            #box = (1022, 360, 1097, 380)  # 设置要裁剪的区域
            box = (745,356,821,376)
            region = im.crop(box)
            region.save(image_path_png)
            username = driver.find_element_by_id("username")
            password = driver.find_element_by_id("password")
            username.clear()
            username.send_keys(settings.LE_USERNAME)
            #username.send_keys("yaoxuzhao")
            password.clear()
            password.send_keys(settings.LE_PASSWORD)
            #password.send_keys("123")
            val_code = driver.find_element_by_id("valCode")
            val_code.clear()
            img_code = img_to_str(image_path_png)
            if not img_code:
                img_code = "abcd"
            val_code.send_keys(img_code)
            time.sleep(3)
            driver.find_element_by_xpath("//input[@type='submit']").click()
            time.sleep(5)
            if driver.find_elements_by_class_name("header_img"):
                break

def get_data(date):
    try:
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_experimental_option('prefs', {
        #     'credentials_enable_service': True,
        #     'profile': {
        #         'password_manager_enabled': True
        #     }
        # })
        # # 读取本地信息
        # chrome_options.add_argument("--user-data-dir=" + USER_DATA_DIR)
        # driver = webdriver.Chrome(chrome_options=chrome_options)
        driver = webdriver.PhantomJS()
        driver.get(BASE_URL)
        time.sleep(6)
        now = datetime.now()
        gs = GetStatisticsDataFromOMS(date)
        gs.login(driver)
        result = gs.get_data(driver)
        gs.clean_data()
        #time.sleep(1000)
    finally:
        driver.quit()

if __name__=="__main__":
    now = datetime.now()
    days = 2
    while days<3:
        date = now-timedelta(days=days)
        date = date.strftime("%Y-%m-%d")
        get_data(date)