from .base import *
from kombu import Queue
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
CELERY_RESULT_BACKEND = 'amqp://lepython:qaz123456@192.168.2.97:5672/dev'
INSTALLED_APPS.append('report')
INSTALLED_APPS.append('monitor')
CHROME_USER_DATA_DIR = r"C:\Users\yaoxuzhao\AppData\Local\Google\Chrome\User Data"
LE_USERNAME = "yaoxuzhao"
LE_PASSWORD = "123"

CELERY_QUEUES = ( # 定义任务队列
        #celery           exchange=celery(direct) key=celery
    Queue('celery', routing_key='celery'), # 路由键以“task.”开头的消息都进default队列
    Queue('web_tasks', routing_key='web.insert_data'), # 路由键以“web.”开头的消息都进web_tasks队列
)
CELERY_DEFAULT_EXCHANGE = 'celery' # 默认的交换机名字为tasks
CELERY_DEFAULT_EXCHANGE_TYPE = 'direct' # 默认的交换类型是topic
CELERY_DEFAULT_ROUTING_KEY = 'celery' # 默认的路由键是task.default，这个路由键符合上面的default队列
CELERY_ROUTES = {
    'monitor.tasks.update_feedback': { # tasks.add的消息会进入web_tasks队列
    'queue': 'web_tasks',
    'routing_key': 'web.insert_data',
    }
}