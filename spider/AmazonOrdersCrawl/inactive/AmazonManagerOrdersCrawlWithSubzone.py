# coding = utf-8
import datetime
import os
import sys
import time
# from datetime import datetime
import datetime
import pandas as pd
import pymysql
from lxml import etree
# import cx_Oracle#操作oracle库
from selenium import webdriver  # selenium 需要自己安装此模块
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from AmazonAutoLoginUserCheck import UserLoginCheck
import logging


"""
模拟登录下载订单管理页面数据
"""

current_path = os.path.abspath('.')

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='AmazonManagerOrdersCrawl.log',
                filemode='w')

_LOGGING = logging.getLogger('AmazonManagerOrdersCrawlDE.py')

sub_zone_amzid_dict = {
	  'Amazon.co.uk':'marketplace_A1F83G8C2ARO7P'
	, 'Amazon.de':'marketplace_A1PA6795UKMFR9'
	, 'Amazon.es':'marketplace_A1RKKUPIHCS9HS'
	, 'Amazon.fr':'marketplace_A13V1IB3VIYZZH'
	, 'Amazon.it':'marketplace_APJ6JRA9NG5V4'
	, 'Non-Amazon CO.UK':'marketplace_AZMDEXL2RVFNN'
	, 'Non-Amazon DE':'marketplace_A38D8NSA03LJTC'
	, 'Non-Amazon ES':'marketplace_AFQLKURYRPEL8'
	, 'Non-Amazon FR':'marketplace_A1ZFFQZ3HTUKT9'
	, 'Non-Amazon IT':'marketplace_A62U237T8HV6N'
}

# change key and value
amzid_sub_zone_dict = {value:key for key,value in sub_zone_amzid_dict.items()}

# url = 'https://sellercentral.amazon.es/gp/homepage.html?'

class AmazonOrderManagerCrawl():
    def __init__(self, zone):
        # if zone == '':
        #     sys.exit(0)
        # else:
        #     self.zone = zone
        self.dbconn = pymysql.connect(
            host="192.168.2.23",
            database="leamazon",
            user="ama_account",
            password="T89ZY#UQWS",
            port=3306,
            charset='utf8'
        )
        self.cur = self.dbconn.cursor()
        self.zone = zone
        self.now_order_cnt = 0
        # ulc = UserLoginCheck(tryNum)
        # ulc.login()
        # self.login_id = ulc.login_id

    def getOrderInfo(self):
        # get username and password
        sqlcmd = "select username as un, AES_DECRYPT(password_encrypt,'andy') as pw, login_url as url from core_amazon_account a where platform = '"+self.zone+"'"
                 # "id = %s" % self.login_id + ";"
        a = pd.read_sql(sqlcmd, self.dbconn)
        if (len(a) > 0):
            username = a["un"][0]
            password = str(a["pw"][0], encoding="utf-8")
            url = a["url"][0]
        else:
            sys.exit(0)

        try:
            driver = webdriver.Chrome(current_path + os.path.sep + 'drive' + os.path.sep + 'chromedriver.exe')

            # open driver and get url
            driver.set_page_load_timeout(200)

            driver.get(url)
            time.sleep(5)
            driver.find_element_by_id("ap_email").clear()
            time.sleep(2)
            driver.find_element_by_id("ap_email").send_keys(username)
            time.sleep(2)
            driver.find_element_by_id("ap_password").send_keys(password)
            time.sleep(2)
            driver.find_element_by_id("signInSubmit").click()
            time.sleep(4)

            # login in complete
            WebDriverWait(driver, 120).until(
                lambda driver: driver.execute_script("return document.readyState") == 'complete')
            time.sleep(2)
            driver.maximize_window()

            sub_zone_url = '/merchant-picker/change-merchant?url=%2F&marketplaceId=A13V1IB3VIYZZH&merchantId=AV7KSH7XB8RNM'
            sub_zone = 'Amazon.fr'

            try:
                sqlcmd = "select max(order_date) as order_date from amazon_report_manager_orders a where zone = '" + self.zone + "' and sub_zone='" + sub_zone + "'"
                order_date_max = pd.read_sql(sqlcmd, self.dbconn)
                if (len(order_date_max) > 0 and order_date_max is not None and order_date_max['order_date'][
                    0] is not None):
                    end = order_date_max['order_date'][0].to_pydatetime().date() + datetime.timedelta(days=1)
                else:
                    end = datetime.date(1985, 8, 6)
            except Exception as e:
                print('--------------------------------error-------------------------')
                print(e)
                print('--------------------------------error-------------------------')

            begin = datetime.date.today()
            d = begin
            days = 1
            while d >= end:

                print(d.strftime('%Y-%m-%d %H:%M:%S'))
                order_date_str = d.strftime('%Y-%m-%d %H:%M:%S')
                startDate = d.strftime('%d/%m/%Y')
                endDate = begin.strftime("%d/%m/%Y")

                self.now_order_cnt = 0
                self.crawlByExactDateAndZone(driver, startDate, endDate, sub_zone_url, sub_zone, order_date_str)

                # orders_by_day = round(self.now_order_cnt/days) + 1
                # max_days = round(10/round(orders_by_day/100))
                # if(max_days < 1):
                #     days = 1
                # else:
                #     days = max_days

                begin = d - datetime.timedelta(days=1)
                delta = datetime.timedelta(days=days)
                d -= delta


        except Exception as e:
            print("--------------------------------error-------------------------")
            print(e)
            print("--------------------------------error-------------------------")
            self.deleteAll(driver)

    def crawlByExactDateAndZone(self, driver, startDate, endDate, sub_zone_url, sub_zone, order_date_str):

        # click order manager menu
        # selector =driver.find_element_by_xpath('//*[@id="sc-mkt-picker-switcher-select"]')
        try:
            selector = driver.find_element_by_id('sc-mkt-picker-switcher-select')
            Select(selector).select_by_value(sub_zone_url)  # 子站
            WebDriverWait(driver, 120).until(
                lambda driver: driver.execute_script("return document.readyState") == 'complete')
            time.sleep(2)
        except Exception as e:
            print('--------------------------------error-------------------------')
            print(e)
            print('--------------------------------error-------------------------')
            pass

        # chose english language
        try:
            selector = driver.find_element_by_id('sc-lang-switcher-header-select')
            Select(selector).select_by_visible_text("English")
            WebDriverWait(driver, 120).until(
                lambda driver: driver.execute_script("return document.readyState") == 'complete')
            time.sleep(2)
        except Exception as e:
            print('--------------------------------error-------------------------')
            print(e)
            print('--------------------------------error-------------------------')
            pass

        # click to 'Manage Orders' menu
        try:
            target_menu = 'Manage Orders'
            target_link = driver.find_elements_by_link_text(target_menu)
            if target_link:
                target_link[0].click()
                WebDriverWait(driver, 120).until(
                    lambda driver: driver.execute_script("return document.readyState") == 'complete')
                time.sleep(2)
            else:
                pass
        except Exception as e:
            print('--------------------------------error-------------------------')
            print(e)
            print('--------------------------------error-------------------------')
            pass

        # click to 'Advanced Search' link
        # try:
        #     target_menu = 'Advanced Search'
        #     target_link = driver.find_elements_by_link_text(target_menu)
        #     if target_link:
        #         target_link[0].click()
        #         WebDriverWait(driver, 120).until(
        #             lambda driver: driver.execute_script("return document.readyState") == 'complete')
        #         time.sleep(2)
        #     else:
        #         pass
        # except Exception as e:
        #     print('--------------------------------error-------------------------')
        #     print(e)
        #     print('--------------------------------error-------------------------')

        # change the begin and end date
        try:
            exactDateBeginStr = startDate
            exactDateEndStr = endDate

            driver.find_element_by_id('_myoSO_SearchOption_exactDates').click()

            # 如果上面的Advanced Search部分有使用的话，这里才会需要，通过JS来修改日历控件中的日期
            # js = "document.getElementById(\'exactDateBegin\').removeAttribute('readonly');document.getElementById(\'exactDateBegin\').setAttribute('value','" + exactDateBeginStr + "');"
            # driver.execute_script(js)
            # js = "document.getElementById(\'exactDateEnd\').removeAttribute('readonly');document.getElementById(\'exactDateEnd\').setAttribute('value','" + exactDateEndStr + "');"
            # driver.execute_script(js)

            driver.find_element_by_id('exactDateBegin').send_keys(exactDateBeginStr)
            driver.find_element_by_id('exactDateEnd').send_keys(exactDateEndStr)

            driver.find_element_by_id(sub_zone_amzid_dict[sub_zone]).click()
            driver.find_element_by_id('_myoSO_SearchButton').click()
            time.sleep(10)
            WebDriverWait(driver, 120).until(
                lambda driver: driver.execute_script("return document.readyState") == 'complete')
        except Exception as e:
            print('--------------------------------error-------------------------')
            print(e)
            print('--------------------------------error-------------------------')
            pass

        # change per page cnt to 100,as 100 is the max size
        try:
            driver.find_element_by_xpath("//select[@name='itemsPerPage']").send_keys(100)
            goList = driver.find_elements_by_xpath("//td/input[@type='image' and contains(@src,'go.')]")  # stop here
            if goList:
                goList[-1].click()  # use -1 index, because it's hard to chose the right 'go' input using xpath
                time.sleep(12)
                WebDriverWait(driver, 120).until(
                    lambda driver: driver.execute_script("return document.readyState") == 'complete')
            else:
                pass
        except Exception as e:
            print('--------------------------------error-------------------------')
            print(e)
            print('--------------------------------error-------------------------')
            pass

        # parse driver.page_source in cycs
        try:
            self.parsePageInfo(driver, sub_zone, startDate, order_date_str)
        except Exception as e:
            print('--------------------------------error-------------------------')
            print(e)
            print('--------------------------------error-------------------------')

    def parsePageInfo(self, driver, sub_zone, startDate, order_date_str):
        content = driver.page_source
        tree = etree.HTML(content)

        # now_order_cnt_str = tree.xpath("//[@id='myo-table']//td[contains(text(),' to ')]")

        orders = tree.xpath("//tr[contains(@id,'row-')]")
        self.now_order_cnt += len(orders)
        for order in orders:
            order_id = order.xpath("./@id")[0].replace('row-', '')

            cust_id = ''
            if order.xpath("./td/input[@class='cust-id']/@value"):
                cust_id = order.xpath("./td/input[@class='cust-id']/@value")[0]
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            latestShipDate_str = ''
            if order.xpath("./td/input[@class='latestShipDate']/@value"):
                latestShipDate_str = order.xpath("./td/input[@class='latestShipDate']/@value")[0]
            x = time.localtime(int(latestShipDate_str))
            latestShipDate = time.strftime('%Y-%m-%d %H:%M:%S', x)

            sqli = "insert into amazon_report_manager_orders(order_id, cust_id, zone, sub_zone, order_date, create_date) values(%s, %s, %s, %s, %s, %s)"
            self.cur.execute(sqli, (order_id, cust_id, self.zone, sub_zone, order_date_str, dt))

        self.dbconn.commit()

        try:
            next_link = driver.find_element_by_xpath(
                "//*[@id='myo-table']//a[@class='myo_list_orders_link' and contains(text(),'Next')]")  #
            if next_link:
                next_link.click()
                time.sleep(2)
                WebDriverWait(driver, 120).until(
                    lambda driver: driver.execute_script("return document.readyState") == 'complete')
                time.sleep(2)
                self.parsePageInfo(driver, sub_zone, startDate, order_date_str)
            else:
                # self.deleteAll(driver)
                return
        except Exception as e:
            print("---------------------------------------------------------------------------------")
            print(e)
            print("---------------------------------------------------------------------------------")

    # def __del__(self):
    #     try:
    #         self.cur.close()
    #         self.dbconn.close()
    #         sys.exit(0)
    #     except Exception as e:
    #         print("--------------------------------error-------------------------")
    #         print(e)
    #         print("--------------------------------error-------------------------")

    def deleteAll(self, driver):
        try:
            self.cur.close()
            self.dbconn.close()
            driver.quit()
            sys.exit(0)
        except Exception as e:
            print("--------------------------------error-------------------------")
            print(e)
            print("--------------------------------error-------------------------")


if __name__ == '__main__':
    amzCrawl = AmazonOrderManagerCrawl("DE")
    amzCrawl.getOrderInfo()

