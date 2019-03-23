#coding: utf-8
'''
django 命令行脚本用, 在py文件里如果有model 直接用命令python a.py 是不能运行的，在a.py顶部导入 import init_django ,再运行python a.py
'''

import os

settings_name = 'DServer.settings'
#try:
#    from online_course_server.dev_settings import *
#    settings_name = 'online_course_server.dev_settings'
#except:
#    settings_name = 'online_course_server.settings'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_name)
os.environ['DJANGO_SETTINGS_MODULE'] = settings_name
import django
django.setup()
