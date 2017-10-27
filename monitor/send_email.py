import smtplib
from email.mime.text import MIMEText
from email.header import Header
from django.shortcuts import render_to_response
sender = "yaoxuzhao@ledbrighter.com"
receiver = "641096898@qq.com"
subject = "python email test"
#smtpserver = "imap.exmail.qq.com"
# smtpserver = "imap.exmail.qq.com"
smtpserver = "smtp.exmail.qq.com"
username = "yaoxuzhao@ledbrighter.com"
password = "qazQAZ123456@"

def send_txt():
    msg = MIMEText('你好','text','utf-8')
    msg['Subject'] = Header(subject,'utf-8')

    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username,password)
    smtp.sendmail(sender,receiver,msg.as_string())
    smtp.quit()

def send_html():
    text = render_to_response("../templates/monitor/email.html",{})
    print(text)
    msg=MIMEText(text,"html",'utf-8')
    msg["Subject"]=subject
    msg["from"] = sender
    msg["to"] = receiver
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username,password)
    smtp.sendmail(sender,receiver,msg.as_string())
    smtp.quit()

if __name__ == "__main__":
    send_html()