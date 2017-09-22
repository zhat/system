from .base import *
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1','localhost','192.168.2.97']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bi_system',
        'USER':'lepython',
        'PASSWORD':'qaz123456',
        'HOST':'192.168.2.97',
        'PORT':'3306',
    }
}
BROKER_URL = 'amqp://lepython:qaz123456@192.168.2.97:5672/production'