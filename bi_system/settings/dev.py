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
BROKER_URL = 'amqp://lepython:qaz123456@192.168.2.97:5672/dev'
INSTALLED_APPS.append('report')
CHROME_USER_DATA_DIR = r"C:\Users\yaoxuzhao\AppData\Local\Google\Chrome\User Data"
LE_USERNAME = "yaoxuzhao"
LE_PASSWORD = "123"