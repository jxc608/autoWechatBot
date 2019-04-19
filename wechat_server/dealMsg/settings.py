"""
Django settings for wechat_server project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os, time
from DServer.settings import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'g&016+pc#vw3=nn@umrr6dx+bj+)=pvl09*7vvb2r8$ru&9&9-'

# SECURITY WARNING: don't run with debug turned on in production!


ROOT_URLCONF = 'wechat_server.dealMsg.urls'


WSGI_APPLICATION = 'wechat_server.dealMsg.wsgi.application'


BASE_LOG_DIR = os.path.join(SERVER_FILE_PATH, "wechat_logs")

LOGGING = {
    'version': 1,  # 保留字
    'disable_existing_loggers': False,  # 禁用已经存在的logger实例
    # 日志文件的格式
    'formatters': {
        # 详细的日志格式
        'standard': {
            'format': '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]'
                      '[%(levelname)s][%(message)s]'
        },
        # 简单的日志格式
        'simple': {
            'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
        },
        # 定义一个特殊的日志格式
        'collect': {
            'format': '%(message)s'
        }
    },
    # 过滤器
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    # 处理器
    'handlers': {
        # 在终端打印
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],  # 只有在Django debug为True时才在屏幕打印日志
            'class': 'logging.StreamHandler',  #
            'formatter': 'simple'
        },
        # 默认的
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "%s_info.log" % (time.strftime("%F", time.localtime()))),  # 日志文件
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 3,  # 最多备份几个
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        # 专门用来记错误日志
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "%s_err.log" % (time.strftime("%F", time.localtime()))),  # 日志文件
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        # 专门定义一个收集特定信息的日志
        'collect': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "%s_collect.log" % (time.strftime("%F", time.localtime()))),
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 5,
            'formatter': 'collect',
            'encoding': "utf-8"
        }
    },
    'loggers': {
       # 默认的logger应用如下配置
        '': {
            'handlers': ['default', 'console', 'error'],  # 上线之后可以把'console'移除
            'level': 'DEBUG',
            'propagate': True,  # 向不向更高级别的logger传递
        },
        # 名为 'collect'的logger还单独处理
        'collect': {
            'handlers': ['console', 'collect'],
            'level': 'INFO',
        }
    },
}

WECHAT_MODE_ONLINE = 'online'
WECHAT_MODE_SERVICE = 'service'

WECHAT_TEXT_URL = '%s/send/text' % WECHAT_SERVER_URL
WECHAT_TEMPLATE_URL = '%s/send/template' % WECHAT_SERVER_URL
# 正常通知
WECHAT_TEMPLATE_SCORE_ADD = 'GUhk3-jzV_OgCHckUVxYMKjUj0eXQSqsUnOQzgT6NwA'
# 上下分
WECHAT_TEMPLATE_SCORE_MINUS = 'GUhk3-jzV_OgCHckUVxYMKjUj0eXQSqsUnOQzgT6NwA'
# 授信
WECHAT_TEMPLATE_SCORE_LIMIT = 'bNchIAQi4Voi2zNpbXUqXr9Q0beIzZucaVOjkjeX1rI'


