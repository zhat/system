import os
import time
import subprocess
from celery import shared_task
from .models import Station,Feedback,FeedbackInfo,AmazonRefShopList
from datetime import datetime,timedelta
from django.core.mail import send_mail,EmailMessage
from django.template import loader
from django.conf import settings
import pandas as pd
from email.mime.image import MIMEImage
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
import logging
from selenium import webdriver

logger = logging.getLogger("django")

@shared_task
def update_feedback():
    feedback_list = FeedbackInfo.objects.all()
    for feedback in feedback_list:
        if not feedback.last_month:
            start_date = feedback.date
            last_month = start_date - timedelta(days=start_date.day-1) if start_date.day-1 else (start_date - timedelta(days=1)).replace(day=1)
            last_month_str = last_month.strftime('%Y-%m-%d')
            last_month_feedback = FeedbackInfo.objects.filter(date=last_month_str). \
                filter(zone=feedback.zone).filter(shop_name=feedback.shop_name)
            if last_month_feedback:
                feedback.last_month = feedback.lifetime - last_month_feedback[0].lifetime
        if not feedback.last_week:
            start_date = feedback.date
            days = start_date.weekday() if start_date.weekday() else 7
            last_week = start_date-timedelta(days=days)
            last_week_str = last_week.strftime('%Y-%m-%d')
            print(start_date,last_week,last_week_str)
            last_week_feedback = FeedbackInfo.objects.filter(date=last_week_str).\
                filter(zone=feedback.zone).filter(shop_name=feedback.shop_name)
            if last_week_feedback:
                feedback.last_week=feedback.lifetime-last_week_feedback[0].lifetime
        if not feedback.last_day:
            start_date = feedback.date
            last_day = start_date - timedelta(days=1)
            last_day_str = last_day.strftime('%Y-%m-%d')
            last_day_feedback = FeedbackInfo.objects.filter(date=last_day_str). \
                filter(zone=feedback.zone).filter(shop_name=feedback.shop_name)
            if last_day_feedback:
                feedback.last_day = feedback.lifetime - last_day_feedback[0].lifetime
        feedback.save()

def feedback_image():
    now = datetime.now()
    last_monday = now if not now.weekday() else now - timedelta(days=now.weekday())
    start_monday = last_monday - timedelta(days=29*7)
    last_monday_str = last_monday.strftime("%Y-%m-%d")
    start_monday_str = start_monday.strftime("%Y-%m-%d")
    zone="us"
    days = pd.date_range(start=start_monday_str, end=last_monday_str,freq="7D")
    dates = [date.strftime("%Y-%m-%d") for date in days]
    if now.weekday():  #今天不是星期一
        dates.pop(0)
        dates.append(now.strftime("%Y-%m-%d"))
    shop_list = AmazonRefShopList.objects.filter(zone=zone).filter(type="feedback")
    shop_name_list = [shop.shop_name for shop in shop_list]
    tuples = [(shop_name, date) for shop_name in shop_name_list for date in dates]
    index = pd.MultiIndex.from_tuples(tuples, names=['shop_name', 'day'])
    data_frame = pd.DataFrame(0, index=index, columns=['last_week'])
    feedback_list = FeedbackInfo.objects.filter(zone=zone).filter(date__in=dates)
    print(feedback_list)
    for feedback in feedback_list:
        print(feedback.shop_name,feedback.date)
        print(feedback.last_week)
        if feedback.last_week:
            #print(feedback.last_week)
            data_frame.loc[(feedback.shop_name, feedback.date.strftime("%Y-%m-%d")), 'last_week'] = int(
                feedback.last_week)
        else:
            #print("no feedback last_week")
            data_frame.loc[(feedback.shop_name, feedback.date.strftime("%Y-%m-%d")), 'last_week'] = 0
    x = range(len(dates))
    # 创建绘图对象，figsize参数可以指定绘图对象的宽度和高度，单位为英寸，一英寸=80px

    #print(data_frame)
    plt.figure(figsize=(24,12))
    plt.xticks(x, dates, rotation=60)
    for shop_name in shop_name_list:
        last_week = list(map(int, data_frame.loc[shop_name]['last_week'].values))
        plt.plot(x, last_week,label=shop_name)
    #plt.show()
    plt.legend(loc='upper center',ncol=3)
    #plt.title("周增长量<br/><br/>")
    base_path = settings.IMAGE_PATH
    base_file_path = os.path.join(base_path,"feedback_line_base{}.png".format(int(time.time())))
    final_file_path = os.path.join(base_path, "feedback_line{}.png".format(int(time.time())))
    plt.savefig(base_file_path)  # 保存图
    im = Image.open(base_file_path)
    box = (200,100,2250,1200)  # 设置要裁剪的区域
    region = im.crop(box)
    region.save(final_file_path)
    return final_file_path

def add_img(src, img_id):
    """
    在富文本邮件模板里添加图片
    :param src:
    :param img_id:
    :return:
    """
    fp = open(src, 'rb')
    msg_image = MIMEImage(fp.read())
    fp.close()
    msg_image.add_header('Content-ID', '<'+img_id+'>')
    return msg_image

@shared_task
def send_email():
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d")
    date_str = now.strftime("%Y%m%d")
    zone_list = AmazonRefShopList.objects.filter(type="feedback").values("zone").distinct().all()
    # print(zone_list)
    zones = [zone['zone'] for zone in zone_list]
    zone_feedback_list =[]
    for zone in zones:
        shop_list = AmazonRefShopList.objects.filter(zone=zone).filter(type="feedback").order_by("shop_name")
        # print(shop_list)
        ordering = 'CASE WHEN shop_name="NEON MART" THEN 1 ELSE 2 END'
        feedback_count_list = FeedbackInfo.objects.filter(date=now_str).filter(zone=zone).extra(
           select={'ordering': ordering}, order_by=('ordering','shop_name'))
        shop_url_dict = dict((shop.shop_name, shop.shop_url) for shop in shop_list)
        feedback_table_data = []
        for feedback_count in feedback_count_list:
            feedback_table_data.append({
                'date': feedback_count.date.strftime("%Y-%m-%d"),
                'shop_name': feedback_count.shop_name,
                'shop_url': shop_url_dict[feedback_count.shop_name],
                'last_30_days': feedback_count.last_30_days,
                'last_90_days': feedback_count.last_90_days,
                'last_12_months': feedback_count.last_12_months,
                'lifetime': feedback_count.lifetime,
                'last_day': feedback_count.last_day,
                'last_week': feedback_count.last_week,
                'last_month': feedback_count.last_month,
                'zone': feedback_count.zone,
            })
        zone_feedback_list.append(feedback_table_data)

    email_template_name = '../templates/monitor/email.html'
    t = loader.get_template(email_template_name)
    context={'zone_feedback_list':zone_feedback_list,'date':now_str}
    html_content = t.render(context)
    #send_mail('Feedback统计'+date_str,
    #          '',
    #          settings.EMAIL_FROM,
    #          settings.EMAIL_TO,
    #          html_message=html_content)

    msg = EmailMessage('Feedback统计'+date_str, html_content, settings.EMAIL_FROM,settings.EMAIL_TO)
    msg.content_subtype = 'html'
    msg.encoding = 'utf-8'
    image_path = feedback_image()
    image = add_img(image_path, 'test_cid')
    msg.attach(image)
    if msg.send():
        return True
    else:
        return False

@shared_task
def execute_crawler(spider):
    now=datetime.now()
    today = now.strftime("%Y-%m-%d")
    old_path = os.getcwd()
    logger.debug(old_path)
    os.chdir(settings.SCRAPY_PROJECT_DIR)
    log_file_name = "%s.log"%(today)
    # cmd = settings.SCRAPY_CMD_PATH+" crawl "+spider+" >> "+os.path.join(settings.SCRAPY_LOG_DIR,spider,log_file_name)+" 2>&1"
    cmd = settings.SCRAPY_CMD_PATH+" crawl "+spider
    logging.debug(cmd)
    subprocess.call(cmd,shell=True)
    os.chdir(old_path)

def get_pict():
    driver = webdriver.PhantomJS()
    try:
        driver.maximize_window()
    except Exception as err:
        print(err)
    driver.get("http://localhost:8000/monitor/feedback_week/")
    time.sleep(3)
    base_path = settings.IMAGE_PATH
    time_str = int(time.time() * 10000000)
    image_path = os.path.join(base_path, "week{}.png".format(time_str))
    image_path_png = os.path.join(base_path, "{}.png".format(time_str))
    driver.get_screenshot_as_file(image_path)  # 比较好理解
    driver.quit()

