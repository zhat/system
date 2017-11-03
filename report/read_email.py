# -*- coding: utf-8 -*-
import poplib
import email
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import re
import os
from django.conf import settings


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def guess_charset(msg):
    # 先从msg对象获取编码:
    charset = msg.get_charset()
    if charset is None:
        # 如果获取不到，再从Content-Type字段获取:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


def get_email_headers(msg):
    # 邮件的From, To, Subject存在于根对象上:
    headers = {}
    for header in ['From', 'To', 'Subject', 'Date']:
        value = msg.get(header, '')
        if value:
            if header == 'Date':
                headers['date'] = value
            if header == 'Subject':
                # 需要解码Subject字符串:
                subject = decode_str(value)
                headers['subject'] = subject
            else:
                # 需要解码Email地址:
                hdr, addr = parseaddr(value)
                name = decode_str(hdr)
                value = u'%s <%s>' % (name, addr)
                if header == 'From':
                    from_address = value
                    headers['from'] = from_address
                else:
                    to_address = value
                    headers['to'] = to_address
    content_type = msg.get_content_type()
    print('head content_type: ', content_type)
    return headers


# indent用于缩进显示:
def get_email_cntent(message, base_save_path):
  j = 0
  content = ''
  attachment_files = []
  for part in message.walk():
    j = j + 1
    file_name = part.get_filename()
    #print(file_name)
    contentType = part.get_content_type()
    #print(contentType)
    # 保存附件
    if file_name: # Attachment
      # Decode filename
      h = email.header.Header(file_name)
      #print(h)
      dh = email.header.decode_header(h)
      #print(dh)
      filename = dh[0][0]
      #print(filename)
      #print(dh[0][1])
      if dh[0][1]: # 如果包含编码的格式，则按照该格式解码
          filename = filename.decode(dh[0][1])
          print(filename)
          filename = filename.encode("utf-8")
          print(type(filename))
      data = part.get_payload(decode=True)
      #filepath = os.path.join(base_save_path,filename)
      att_file = open(base_save_path, 'wb')
      attachment_files.append(filename)
      att_file.write(data)
      att_file.close()
    #elif contentType == 'text/plain' or contentType == 'text/html':
      # 保存正文
    #  data = part.get_payload(decode=True)
    #  print(data)
    #  charset = guess_charset(part)
    #  if charset:
    #    charset = charset.strip().split(';')[0]
    #    print ('charset:', charset)
    #    data = data.decode(charset)
    #  content = data
  return content, attachment_files


def get_email_excel():
    # 输入邮件地址, 口令和POP3服务器地址:
    emailaddress = settings.EMAIL_HOST_USER
    # 注意使用开通POP，SMTP等的授权码
    password = settings.EMAIL_HOST_PASSWORD
    pop3_server = settings.EMAIL_HOST

    # 连接到POP3服务器:
    try:
        server = poplib.POP3(pop3_server)
        # 可以打开或关闭调试信息:
        # server.set_debuglevel(1)
        # POP3服务器的欢迎文字:
        print(server.getwelcome())
        # 身份认证:
        server.user(emailaddress)
        server.pass_(password)
        # stat()返回邮件数量和占用空间:
        messagesCount, messagesSize = server.stat()
        print('messagesCount:', messagesCount)
        print('messagesSize:', messagesSize)
        # list()返回所有邮件的编号:
        resp, mails, octets = server.list()
        print('------ resp ------')
        print(resp)  # +OK 46 964346 响应的状态 邮件数量 邮件占用的空间大小
        print('------ mails ------')
        print(mails)  # 所有邮件的编号及大小的编号list，['1 2211', '2 29908', ...]
        print('------ octets ------')
        print(octets)

        # 获取最新一封邮件, 注意索引号从1开始:
        length = len(mails)
        print(length)
        for i in range(length, 1, -1):
            resp, lines, octets = server.retr(i)
            # lines存储了邮件的原始文本的每一行,
            # 可以获得整个邮件的原始文本:
            print(resp)
            # print('222222222222222222222')
            # print(lines)
            # print('222222222222222222222')
            print(octets)
            msg_content = '\n'.join([line.decode("utf-8") for line in lines])
            #msg_content = '\n'.join(lines)
            # print(msg_content)
            # 把邮件内容解析为Message对象：
            msg = Parser().parsestr(msg_content)
            # print(msg)
            # 但是这个Message对象本身可能是一个MIMEMultipart对象，即包含嵌套的其他MIMEBase对象，
            # 嵌套可能还不止一层。所以我们要递归地打印出Message对象的层次结构：
            print('---------- 解析之后 ----------')
            base_save_path = settings.IMAGE_PATH
            msg_headers = get_email_headers(msg)
            # print(msg_headers)
            pattern = re.compile(r"(库存管理总表\d{8})")

            print('subject:', msg_headers['subject'])
            match = re.search(pattern, msg_headers['subject'])
            print(match)
            if match:
                print(match.group())
                filepath = os.path.join(base_save_path,'{}.xlsx'.format(match.group(0)))
                print(filepath)
                if os.path.exists(filepath):
                    break
                content, attachment_files = get_email_cntent(msg, filepath)
            print('from_address:', msg_headers['from'])
            print('to_address:', msg_headers['to'])
            # if hasattr(msg_headers, 'date'):
            #    print('date:', msg_headers['date'])
            # print('content:', content)
            # print('attachment_files: ', attachment_files)
    finally:
        # 关闭连接:
        server.quit()

if __name__ == '__main__':
    get_email_excel()