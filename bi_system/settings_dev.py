"""
Django settings for bi_system project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from kombu import Queue

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rx6h^!7y0z-61-u_#o5bq%twi(u9wn7#@yzm+7nf0j7+)u#cyj'
#SECRET_KEY = ""
# SECURITY WARNING: don't run with debug turned on in production!

# Application definition

DEBUG = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap3',
    'spider',
    'order',
    'djcelery',
    'kombu.transport.django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bi_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bi_system.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(BASE_DIR,'static')
STATICFILES_DIRS=(
    os.path.join(BASE_DIR,'static'),
)

MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join(BASE_DIR,'media')

LOGIN_URL='/users/login/'

#BROKER_URL = 'django://localhost:8000//'

CELERYD_CONCURRENCY = 1  # 并发worker数
CELERYD_MAX_TASKS_PER_CHILD = 100    # 每个worker最多执行10个任务就会被销毁，可防止内存泄露
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

#SECRET_KEY = 'rx6h^!7y0z-61-u_#o5bq%twi(u9wn7#@yzm+7nf0j7+)u#cyj'
ALLOWED_HOSTS = ['127.0.0.1','localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bi_system_dev',
        'USER':'lepython',
        'PASSWORD':'qaz123456',
        'HOST':'192.168.2.97',
        'PORT':'3306',
    },
    ###"mysql://ama_account:T89ZY#UQWS@192.168.2.23:3306/leamazon/"
    'remote': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'leamazon',
        'USER':'ama_account',
        'PASSWORD':'T89ZY#UQWS',
        'HOST':'192.168.2.23',
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

BROKER_URL = 'amqp://lepython:qaz123456@192.168.2.97:5672/dev'
CELERY_RESULT_BACKEND = 'amqp://lepython:qaz123456@192.168.2.97:5672/dev'
LOGIN_REDIRECT_URL="/"
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
    },
    'monitor.tasks.send_email': { # tasks.add的消息会进入web_tasks队列
    'queue': 'web_tasks',
    'routing_key': 'web.insert_data',
    },
    'report.tasks.clean': { # tasks.add的消息会进入web_tasks队列
    'queue': 'web_tasks',
    'routing_key': 'web.insert_data',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.exmail.qq.com'
EMAIL_PORT = 465
#发送邮件的邮箱
EMAIL_HOST_USER = 'yaoxuzhao@ledbrighter.com'
#在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = 'qazQAZ123456@'
#收件人看到的发件人
EMAIL_FROM = 'yaoxuzhao@ledbrighter.com'
#EMAIL_TO = ['fuqiang@ledbrighter.com','leo@leinaled.com','yangzhixiang@ledbrighter.com','yaoxuzhao@ledbrighter.com']
EMAIL_TO = ['yaoxuzhao@ledbrighter.com']
EMAIL_TIMEOUT = 20

#
IMAGE_PATH = os.path.join(BASE_DIR,"images")

#logging日志配置
LOGGING = {
 'version': 1,
 'disable_existing_loggers': True,
 'formatters': {#日志格式
 'standard': {
  'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'}
 },
 'filters': {#过滤器
 'require_debug_false': {
  '()': 'django.utils.log.RequireDebugFalse',
  }
 },
 'handlers': {#处理器
 'null': {
  'level': 'DEBUG',
  'class': 'logging.NullHandler',
 },
 'debug': {#记录到日志文件(需要创建对应的目录，否则会出错)
  'level':'DEBUG',
  'class':'logging.handlers.RotatingFileHandler',
  'filename': os.path.join(BASE_DIR, "log",'debug.log'),#日志输出文件
  'maxBytes':1024*1024*5,#文件大小
  'backupCount': 5,#备份份数
  'formatter':'standard',#使用哪种formatters日志格式
 },
 'console':{#输出到控制台
  'level': 'DEBUG',
  'class': 'logging.StreamHandler',
  'formatter': 'standard',
 },
 },
 'loggers': {#logging管理器
 'django': {
  'handlers': ['console','debug'],
  'level': 'INFO',
  'propagate': False
 },
 'django.request': {
  'handlers': ['debug'],
  'level': 'DEBUG',
  'propagate': True,
 },
 # 对于不在 ALLOWED_HOSTS 中的请求不发送报错邮件
 'django.security.DisallowedHost': {
  'handlers': ['null'],
  'propagate': False,
 },
 }
}