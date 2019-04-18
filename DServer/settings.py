# -*- coding: utf-8 -*-

"""
Django settings for DServer project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from hashring import *

import logging
import django.utils.log
import logging.handlers
import time

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'r62_a1o23l0j+-^u)q^37*t3e0sdltax5e11dv0vq)#jmha(3m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
if DEBUG:
    SERVER_FILE_PATH = BASE_DIR
else:
    SERVER_FILE_PATH = '/opt/wechat_files'

ALLOWED_HOSTS = ['*']

DATA_UPLOAD_MAX_NUMBER_FIELDS = None
# Application definition

INSTALLED_APPS = [
    'DServerAPP.apps.DserverappConfig',
    'admin_view_permission',
    'grappelli',
    'daterange_filter',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_crontab',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'uadetector.django.middleware.UADetectorMiddleware',
]

ROOT_URLCONF = 'DServer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'DServer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DB_PWD = 'autoAccounting1989'
if DEBUG:
    DB_PWD = '38211108'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'auto_accounting',
        'USER': 'root',
        'PASSWORD': DB_PWD,
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {'charset':'utf8mb4'},
    }
}

# session 设置
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # 引擎（默认）
SESSION_COOKIE_AGE = 1209600  # Session的cookie失效日期（2周）（默认）
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # 是否关闭浏览器使得Session过期（默认）
SESSION_SAVE_EVERY_REQUEST = True  # 是否每次请求都保存Session，默认修改之后才保存（默认）

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

BASE_LOG_DIR = os.path.join(SERVER_FILE_PATH, "logs")

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
            'maxBytes': 1024 * 1024 * 1000,  # 日志大小 50M
            'backupCount': 3,  # 最多备份几个
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        # 专门用来记错误日志
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "%s_err.log" % (time.strftime("%F", time.localtime()))),  # 日志文件
            'maxBytes': 1024 * 1024 * 1000,  # 日志大小 50M
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        # 专门定义一个收集特定信息的日志
        'collect': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "%s_collect.log" % (time.strftime("%F", time.localtime()))),
            'maxBytes': 1024 * 1024 * 1000,  # 日志大小 50M
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

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(SERVER_FILE_PATH, 'static')

# 最简单配置
CRONJOBS = [
    # 表示每天2：01执行
    ('0 0 * * *', 'blog.core.task')
]

GRAPPELLI_ADMIN_TITLE = "机器人后台管理系统"

#机器人进程
if DEBUG:
    BOT_SERVERS = ['http://127.0.0.1:8081']
else:
    BOT_SERVERS = ['http://wbot_server.leafsnow.xyz']

BOT_RING = HashRing(BOT_SERVERS)
BOT_KEY = 'We1kskbot2018'

WECHAT_SERVER_URL = 'http://wechat.leafsnow.xyz'
if DEBUG:
    WECHAT_SERVER_URL = 'http://127.0.0.1:9000'
WECHAT_QRCODE_ADD = '%s/qrcode/add' % WECHAT_SERVER_URL
