from .base import *

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','localhost','192.168.2.98']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bi_system_dev',
        'USER':'lepython',
        'PASSWORD':'qaz123456',
        'HOST':'192.168.2.97',
        'PORT':'3306',
    }
}
TASKS_DATABASE = {
            'host':"192.168.2.97",
            'database':"bi_system_dev",
            'user':"lepython",
            'password':"qaz123456",
            'port':3306,
            'charset':'utf8'
}
LOGIN_REDIRECT_URL="/"
BROKER_URL = 'amqp://lepython:qaz123456@192.168.2.97:5672/dev'
INSTALLED_APPS.append('report')
INSTALLED_APPS.append('monitor')
CHROME_USER_DATA_DIR = r"C:\Users\yaoxuzhao\AppData\Local\Google\Chrome\User Data"
LE_USERNAME = "yaoxuzhao"
LE_PASSWORD = "123"