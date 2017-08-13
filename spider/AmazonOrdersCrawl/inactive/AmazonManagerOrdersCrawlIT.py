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
# from AmazonAutoLoginUserCheck import UserLoginCheck
import logging
from selenium.webdriver.chrome.options import Options

"""
模拟登录下载订单管理页面数据_IT
"""

current_path = os.path.abspath('.')

logging.basicConfig(level=logging.ERROR,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %Y-%m-%d  %H:%M:%S',
                filename='AmazonManagerOrdersCrawlIT.log',
                filemode='w')

_LOGGING = logging.getLogger('AmazonManagerOrdersCrawlIT.py')

marketplaceid_dict = {
	  'co.uk':'A1F83G8C2ARO7P'
	, 'de':'A1PA6795UKMFR9'
	, 'es':'A1RKKUPIHCS9HS'
	, 'fr':'A13V1IB3VIYZZH'
	, 'it':'APJ6JRA9NG5V4'
	, 'Non-Amazon CO.UK':'AZMDEXL2RVFNN'
	, 'Non-Amazon DE':'A38D8NSA03LJTC'
	, 'Non-Amazon ES':'AFQLKURYRPEL8'
	, 'Non-Amazon FR':'A1ZFFQZ3HTUKT9'
	, 'Non-Amazon IT':'A62U237T8HV6N'
}

merchantId_dict = {
    'de':'AV7KSH7XB8RNM'
}

# for example
# /merchant-picker/change-merchant?url=%2F&marketplaceId=A1F83G8C2ARO7P&merchantId=AV7KSH7XB8RNM
# '/merchant-picker/change-merchant?url=%2F&marketplaceId=' + marketplaceid_dict[zone] + '&merchantId=' +  merchantId_dict[zone]


# change key and value
amzid_marketplace_dict = {value:key for key,value in marketplaceid_dict.items()}

# url = 'https://sellercentral.amazon.es/gp/homepage.html?'

class AmazonOrderManagerCrawl():
    def __init__(self, zone, tryCnt):
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
        self.now_date_str = ''
        self.tryCnt = tryCnt
        self.crawlWrongDate = False
        self.now_sub_zone = ''
        # ulc = UserLoginCheck(tryNum)
        # ulc.login()
        # self.login_id = ulc.login_id

    def getOrderInfo(self):
        # get username and password
        sqlcmd = "select username as un, AES_DECRYPT(password_encrypt,'andy') as pw, login_url as url from core_amazon_account a where department = '技术部' and platform = '"+self.zone+"'"
                 # "id = %s" % self.login_id + ";"
        a = pd.read_sql(sqlcmd, self.dbconn)
        if (len(a) > 0):
            username = a["un"][0]
            password = str(a["pw"][0], encoding="utf-8")
            url = a["url"][0]
        else:
            sys.exit(0)

        chrome_options = Options()
        chrome_options.add_experimental_option('prefs', {
            'credentials_enable_service': False,
            'profile': {
                'password_manager_enabled': False
            }
        })
        # driver = webdriver.Chrome(current_path + os.path.sep + 'drive' + os.path.sep + 'chromedriver.exe')
        driver = webdriver.Chrome(executable_path='D:\\andy_yang\\projects\\AmazonPaymentGenerator\\drive\\chromedriver.exe', chrome_options=chrome_options)
        try:

            # open driver and get url
            driver.set_page_load_timeout(200)

            driver.get(url)
            time.sleep(5)

            driver.refresh()
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

            driver.refresh()
            time.sleep(5)

            # sub_zone_url = '/merchant-picker/change-merchant?url=%2F&marketplaceId=' + marketplaceid_dict[self.zone.lower()] + '&merchantId=' +  merchantId_dict[self.zone.lower()]
            sub_zone_url = ''
            sub_zone = ''

            # if have wrong data, then recrawl them
            if self.crawlWrongDate:
                try:

                    insert_exists_date = "insert into amazon_report_total_orders_source_it(zone, order_date, total_cnt) " \
                                         "select '" + self.zone + "', order_date, total_cnt " \
                                                                  "  from amazon_report_order_manager_recrawl_it a " \
                                                                  " where not exists (select 1 from (select zone,order_date,sum(total_cnt) as total_cnt from amazon_report_total_orders_source_it group by 1,2 order by 1,2) b" \
                                                                  "  where a.zone = b.zone" \
                                                                  "    and a.order_date = b.order_date)"
                    self.cur.execute(insert_exists_date)
                    self.dbconn.commit()

                    clear_wrong_data = "delete from amazon_report_order_manager_recrawl_it"
                    self.cur.execute(clear_wrong_data)
                    self.dbconn.commit()

                    create_recrawl_list = "insert into amazon_report_order_manager_recrawl_it(order_date, zone, cnt, total_cnt) " \
                                          "select a.order_date , a.zone , case when b.cnt is not null then a.total_cnt - b.cnt else a.total_cnt end as cnt, a.total_cnt" \
                                          "  from (select zone,order_date,sum(total_cnt) as total_cnt from amazon_report_total_orders_source_it group by 1,2 order by 1,2) a" \
                                          "  left join (select order_date,zone,count(distinct order_id) as cnt from amazon_report_manager_orders_it group by 1,2) b" \
                                          " on a.order_date = b.order_date " \
                                          "   and a.zone = b.zone" \
                                          "   where b.order_date is NULL or a.total_cnt <> b.cnt"
                    self.cur.execute(create_recrawl_list)
                    self.dbconn.commit()

                    delete_exists_data_1 = "delete from amazon_report_manager_orders_it " \
                                           " where order_date in (select distinct order_date from amazon_report_order_manager_recrawl_it)" \
                                           "   and zone = '"+self.zone+"'"
                    self.cur.execute(delete_exists_data_1)
                    self.dbconn.commit()

                    delete_exists_data_2 = "delete from amazon_report_total_orders_source_it " \
                                           " where order_date in (select distinct order_date from amazon_report_order_manager_recrawl_it)" \
                                           "   and zone = '"+self.zone+"'"
                    self.cur.execute(delete_exists_data_2)
                    self.dbconn.commit()

                    select_recrawl_list_query = "select distinct order_date from amazon_report_order_manager_recrawl_it"
                    select_recrawl_list = pd.read_sql(select_recrawl_list_query, self.dbconn)

                    date_list = select_recrawl_list['order_date'].tolist()
                    date_list_len = date_list.__len__()
                    while date_list_len > 0:
                        startDate = date_list[date_list_len-1].to_pydatetime().date().strftime('%d/%m/%Y')
                        endDate = date_list[date_list_len-1].to_pydatetime().date().strftime('%d/%m/%Y')
                        order_date_str = date_list[date_list_len-1].to_pydatetime().date().strftime('%Y-%m-%d %H:%M:%S')
                        self.crawlByExactDateAndZone(driver, startDate, endDate, sub_zone_url, sub_zone, order_date_str)
                        date_list_len -= 1
                except Exception as e:
                    _LOGGING.error(e)


            # crawl data day by day
            try:
                # sqlcmd = "select max(order_date) as order_date from amazon_report_manager_orders_it a where zone = '" + self.zone + "'"
                sqlcmd = "select min(order_date) as order_date from amazon_report_manager_orders_it a where zone = '" + self.zone + "'"
                order_date_max = pd.read_sql(sqlcmd, self.dbconn)
                if (len(order_date_max) > 0 and order_date_max is not None and order_date_max['order_date'][
                    0] is not None):
                    begin = order_date_max['order_date'][0].to_pydatetime().date() - datetime.timedelta(days=1)
                else:
                    begin = datetime.date.today()
                    # sys.exit(0)
            except Exception as e:
                _LOGGING.error(e)

            # begin = datetime.date.today()
            # begin = datetime.date(2017, 3, 9)
            end = datetime.date(1985, 4, 10)

            # for debug
            # begin = datetime.date(2016, 12, 16)
            # end = datetime.date(2016, 12, 16)

            d = begin
            days = 1



            while d >= end and self.tryCnt>0:
                # print(d.strftime('%Y-%m-%d %H:%M:%S'))
                order_date_str = d.strftime('%Y-%m-%d %H:%M:%S')
                startDate = d.strftime('%d/%m/%Y')
                endDate = begin.strftime("%d/%m/%Y")

                self.now_order_cnt = 0
                self.crawlByExactDateAndZone(driver, startDate, endDate, sub_zone_url, sub_zone, order_date_str)

                begin = d - datetime.timedelta(days=1)
                delta = datetime.timedelta(days=days)
                d -= delta

                self.tryCnt -= 1

        except Exception as e:
            _LOGGING.error(e)
            self.deleteAll(driver)

    def crawlByExactDateAndZone(self, driver, startDate, endDate, sub_zone_url, sub_zone, order_date_str):

        # chose the zone
        selector =driver.find_element_by_xpath('//*[@id="sc-mkt-picker-switcher-select"]')
        try:
            selector = driver.find_element_by_id('sc-mkt-picker-switcher-select')
            Select(selector).select_by_value(sub_zone_url)  # 子站
            WebDriverWait(driver, 120).until(
                lambda driver: driver.execute_script("return document.readyState") == 'complete')
            time.sleep(2)
        except Exception as e:
            _LOGGING.error(e)
            pass

        # chose english language
        try:
            selector = driver.find_element_by_id('sc-lang-switcher-header-select')
            Select(selector).select_by_visible_text("English")
            WebDriverWait(driver, 120).until(
                lambda driver: driver.execute_script("return document.readyState") == 'complete')
            time.sleep(2)
        except Exception as e:
            _LOGGING.error(e)
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
            _LOGGING.error(e)
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
        #     _LOGGING.error(e)

        # change the begin and end date
        try:
            exactDateBeginStr = startDate
            exactDateEndStr = endDate

            # driver.find_element_by_id('_myoSO_SearchOption_exactDates').click()
            _myoLO_SearchTypeSelect = driver.find_element_by_id('_myoLO_SearchTypeSelect')
            Select(_myoLO_SearchTypeSelect).select_by_value('DateRange')

            _myoLO_preSelectedRangeSelect = driver.find_element_by_id('_myoLO_preSelectedRangeSelect')
            Select(_myoLO_preSelectedRangeSelect).select_by_value('exactDates')

            # 如果上面的Advanced Search部分有使用的话，这里才会需要，通过JS来修改日历控件中的日期
            js = "document.getElementById(\'exactDateBegin\').removeAttribute('readonly');document.getElementById(\'exactDateBegin\').setAttribute('value','" + exactDateBeginStr + "');"
            driver.execute_script(js)
            js = "document.getElementById(\'exactDateEnd\').removeAttribute('readonly');document.getElementById(\'exactDateEnd\').setAttribute('value','" + exactDateEndStr + "');"
            driver.execute_script(js)

            # driver.find_element_by_id('exactDateBegin').send_keys(exactDateBeginStr)
            # driver.find_element_by_id('exactDateEnd').send_keys(exactDateEndStr)

            # driver.find_element_by_id(sub_zone_amzid_dict[sub_zone]).click()

            driver.find_element_by_id('SearchID').click()

            # handle system error
            self.systemErrorHandle(driver, 5)
            self.waitForLoadData(driver, 5)

            time.sleep(15)

            WebDriverWait(driver, 120).until(
                lambda driver: driver.execute_script("return document.readyState") == 'complete')

            # handle searching error
            content = driver.page_source
            tree = etree.HTML(content)
            search_result = tree.xpath('//*[@id="_myoV2PageTopMessagePlaceholder"]//text()')
            style = tree.xpath('//*[@id="_myoV2PageTopMessagePlaceholder"]/@style')
            search_result_str = ''
            if search_result is not None and len(search_result) > 0:
                for str in search_result:
                    search_result_str += str
                print(search_result_str)

            if 'Too Many Orders Found' in search_result_str and (style is None or len(style) == 0 or 'display' not in style[0]):
                _myoLO_SearchTypeSelect = driver.find_element_by_id('_myoLO_SearchTypeSelect')
                Select(_myoLO_SearchTypeSelect).select_by_value('Marketplace')
                salesChannels = tree.xpath('//*[@id="_myoLO_marketplaceFilterSelect"]/option/@value')
                for salesChannel in salesChannels:
                    if salesChannel != 'sitesall':
                        _myoLO_marketplaceFilterSelect = driver.find_element_by_id('_myoLO_marketplaceFilterSelect')
                        Select(_myoLO_marketplaceFilterSelect).select_by_value(salesChannel)

                        _myoLO_preSelectedRangeSelect = driver.find_element_by_id('_myoLO_preSelectedRangeSelect')
                        Select(_myoLO_preSelectedRangeSelect).select_by_value('exactDates')

                        # 如果上面的Advanced Search部分有使用的话，这里才会需要，通过JS来修改日历控件中的日期
                        js = "document.getElementById(\'exactDateBegin\').removeAttribute('readonly');document.getElementById(\'exactDateBegin\').setAttribute('value','" + exactDateBeginStr + "');"
                        driver.execute_script(js)
                        js = "document.getElementById(\'exactDateEnd\').removeAttribute('readonly');document.getElementById(\'exactDateEnd\').setAttribute('value','" + exactDateEndStr + "');"
                        driver.execute_script(js)

                        driver.find_element_by_id('SearchID').click()

                        # handle system error
                        self.systemErrorHandle(driver, 5)

                        time.sleep(15)

                        WebDriverWait(driver, 120).until(
                            lambda driver: driver.execute_script("return document.readyState") == 'complete')

                        # handle searching error
                        content = driver.page_source
                        tree = etree.HTML(content)
                        search_result = tree.xpath('//*[@id="_myoV2PageTopMessagePlaceholder"]//text()')
                        style = tree.xpath('//*[@id="_myoV2PageTopMessagePlaceholder"]/@style')
                        search_result_str = ''
                        if search_result is not None and len(search_result) > 0:
                            for str in search_result:
                                search_result_str += str
                            print(search_result_str)

                        if 'No Order Found' in search_result_str and (style is None or len(style) == 0 or 'display' not in style[0]):
                            continue

                        sub_zone = amzid_marketplace_dict[salesChannel]
                        self.crawlBySalesChannel(driver, startDate, endDate, sub_zone_url, sub_zone, order_date_str, salesChannel)
            elif 'No Order Found' in search_result_str and (style is None or len(style) == 0 or 'display' not in style[0]):
                return
            else:
                pass

        except Exception as e:
            _LOGGING.error(e)
            pass

        # change per page cnt to 100,as 100 is the max size
        try:
            driver.find_element_by_xpath("//select[@name='itemsPerPage']").send_keys(100)
            goList = driver.find_elements_by_xpath("//td/input[@type='image' and contains(@src,'go.')]")  # stop here
            if goList:
                goList[-1].click()  # use -1 index, because it's hard to chose the right 'go' input using xpath
                time.sleep(15)
                WebDriverWait(driver, 120).until(
                    lambda driver: driver.execute_script("return document.readyState") == 'complete')

                content = driver.page_source
                tree = etree.HTML(content)
                if (tree.xpath("//select[@name='itemsPerPage']/option[@selected]/@value")[0] != '100'):
                    times = 3
                    while times>0:
                        driver.find_element_by_xpath("//select[@name='itemsPerPage']").send_keys(100)
                        goList = driver.find_elements_by_xpath(
                            "//td/input[@type='image' and contains(@src,'go.')]")  # stop here
                        if goList:
                            goList[
                                -1].click()  # use -1 index, because it's hard to chose the right 'go' input using xpath
                            time.sleep(15)
                            WebDriverWait(driver, 120).until(
                                lambda driver: driver.execute_script("return document.readyState") == 'complete')

                        content = driver.page_source
                        tree = etree.HTML(content)
                        if (tree.xpath("//select[@name='itemsPerPage']/option[@selected]/@value")[0] == '100'):
                            break

                        times -= 1

            else:
                pass
        except Exception as e:
            _LOGGING.error(e)
            pass

        # parse driver.page_source in cycs
        try:
            self.parsePageInfo(driver, sub_zone, startDate, order_date_str)
        except Exception as e:
            _LOGGING.error(e)

    def crawlBySalesChannel(self, driver, startDate, endDate, sub_zone_url, sub_zone, order_date_str, salesChannel):
        # change per page cnt to 100,as 100 is the max size
        try:
            driver.find_element_by_xpath("//select[@name='itemsPerPage']").send_keys(100)
            goList = driver.find_elements_by_xpath("//td/input[@type='image' and contains(@src,'go.')]")  # stop here
            if goList:
                goList[-1].click()  # use -1 index, because it's hard to chose the right 'go' input using xpath
                time.sleep(15)
                WebDriverWait(driver, 120).until(
                    lambda driver: driver.execute_script("return document.readyState") == 'complete')

                content = driver.page_source
                tree = etree.HTML(content)
                if (tree.xpath("//select[@name='itemsPerPage']/option[@selected]/@value")[0] != '100'):
                    times = 3
                    while times > 0:
                        driver.find_element_by_xpath("//select[@name='itemsPerPage']").send_keys(100)
                        goList = driver.find_elements_by_xpath(
                            "//td/input[@type='image' and contains(@src,'go.')]")  # stop here
                        if goList:
                            goList[
                                -1].click()  # use -1 index, because it's hard to chose the right 'go' input using xpath
                            time.sleep(15)
                            WebDriverWait(driver, 120).until(
                                lambda driver: driver.execute_script("return document.readyState") == 'complete')

                        content = driver.page_source
                        tree = etree.HTML(content)
                        if (tree.xpath("//select[@name='itemsPerPage']/option[@selected]/@value")[0] == '100'):
                            break

                        times -= 1
            else:
                pass

            self.parsePageInfo(driver, sub_zone, startDate, order_date_str)
        except Exception as e:
            _LOGGING.error(e)


    def parsePageInfo(self, driver, sub_zone, startDate, order_date_str):
        content = driver.page_source
        tree = etree.HTML(content)

        try:
            if sub_zone != self.now_sub_zone:
                dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                now_order_cnt_str = tree.xpath(
                    '//*[@id="myo-table"]/table/tbody/tr[1]/td/table/tbody/tr/td[1]/strong[2]/text()')
                now_order_cnt = int(now_order_cnt_str[0])
                total_cnt_query = "insert into amazon_report_total_orders_source_it(zone, sub_zone, order_date, total_cnt, create_date) values(%s, %s, %s, %s, %s)"
                self.cur.execute(total_cnt_query, (self.zone, sub_zone, order_date_str, now_order_cnt, dt))
                self.now_date_str = order_date_str
                self.now_sub_zone = sub_zone
            elif order_date_str != self.now_date_str:
                dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                now_order_cnt_str = tree.xpath(
                    '//*[@id="myo-table"]/table/tbody/tr[1]/td/table/tbody/tr/td[1]/strong[2]/text()')
                now_order_cnt = int(now_order_cnt_str[0])
                total_cnt_query = "insert into amazon_report_total_orders_source_it(zone, order_date, total_cnt, create_date) values(%s, %s, %s, %s)"
                self.cur.execute(total_cnt_query, (self.zone, order_date_str, now_order_cnt, dt))
                self.now_date_str = order_date_str
            else:
                pass

        except Exception as e:
            _LOGGING.error(e)


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

            sqli = "insert into amazon_report_manager_orders_it(order_id, cust_id, zone, order_date, create_date) values(%s, %s, %s, %s, %s)"
            self.cur.execute(sqli, (order_id, cust_id, self.zone, order_date_str, dt))

        self.dbconn.commit()

        try:
            next_link = driver.find_element_by_xpath(
                "//*[@id='myo-table']//a[@class='myo_list_orders_link' and contains(text(),'Next')]")  #
            if next_link:
                next_link.click()
                WebDriverWait(driver, 120).until(
                    lambda driver: driver.execute_script("return document.readyState") == 'complete')
                time.sleep(15)

                self.waitForLoadData(driver, 5)

                self.parsePageInfo(driver, sub_zone, startDate, order_date_str)

            else:
                # self.deleteAll(driver)
                return
        except Exception as e:
            _LOGGING.error(e)

    def waitForLoadData(self, driver, waitSeconds):
        try:
            content = driver.page_source
            tree = etree.HTML(content)
            _myoLO_pleaseWaitExtendedMessage = tree.xpath('//*[@id="_myoLO_pleaseWaitExtendedMessage"]//text()')
            style = tree.xpath('//*[@id="_myoLO_pleaseWaitExtendedMessage"]/@style')
            _myoLO_pleaseWaitExtendedMessage_str = ''
            if _myoLO_pleaseWaitExtendedMessage is not None and len(_myoLO_pleaseWaitExtendedMessage) > 0:
                for str in _myoLO_pleaseWaitExtendedMessage:
                    _myoLO_pleaseWaitExtendedMessage_str += str
                print(_myoLO_pleaseWaitExtendedMessage_str)

            if 'We apologize for the delay' in _myoLO_pleaseWaitExtendedMessage_str and (
                                style is None or len(style) == 0 or 'display' not in style[0]):
                time.sleep(waitSeconds)
        except Exception as e:
            _LOGGING(e)

    def systemErrorHandle(self, driver, waitSeconds):
        try:
            content = driver.page_source
            tree = etree.HTML(content)
            _myoLO_pleaseWaitExtendedMessage = tree.xpath('//*[@id="_myoV2_AjaxGenericSysErrorMessagePlaceholder"]//text()')
            style = tree.xpath('//*[@id="_myoV2_AjaxGenericSysErrorMessagePlaceholder"]/@style')
            _myoLO_pleaseWaitExtendedMessage_str = ''
            if _myoLO_pleaseWaitExtendedMessage is not None and len(_myoLO_pleaseWaitExtendedMessage) > 0:
                for str in _myoLO_pleaseWaitExtendedMessage:
                    _myoLO_pleaseWaitExtendedMessage_str += str
                print(_myoLO_pleaseWaitExtendedMessage_str)

            if style is None or len(style) == 0 or 'display' not in style[0]:
                # time.sleep(waitSeconds)
                sys.exit(0)
        except Exception as e:
            _LOGGING(e)



    # def __del__(self):
    #     try:
    #         self.cur.close()
    #         self.dbconn.close()
    #         sys.exit(0)
    #     except Exception as e:
    #        _LOGGING.error(e)

    def deleteAll(self, driver):
        try:
            self.cur.close()
            self.dbconn.close()
            driver.quit()
            sys.exit(0)
        except Exception as e:
            _LOGGING.error(e)


# if __name__ == '__main__':
#     amzCrawl = AmazonOrderManagerCrawl("DE", 2)
#     amzCrawl.getOrderInfo()

amzCrawl = AmazonOrderManagerCrawl("IT", 45)
amzCrawl.crawlWrongDate = True
amzCrawl.getOrderInfo()

