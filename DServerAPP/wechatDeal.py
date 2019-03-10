#coding=utf-8
import json
import traceback
from .models import Clubs, Manager, Player

import threading
import time
import inspect
import ctypes
import logging
from django.conf import settings
import requests

logger = logging.getLogger(__name__)

_list = {}


def wechat_request(url, params, method='GET'):
    wid = params["wid"]
    club_name = wid.split('__,__')[0]
    params["wid"] = club_name
    club = Clubs.objects.get(user_name=club_name)
    server = settings.BOT_RING.get_node(str(club.uuid))
    url = '%s%s' % (server, url)
    params['key'] = settings.BOT_KEY
    if method == 'GET':
        res = requests.get(url=url, params=params)
    elif method == 'POST':
        res = requests.post(url=url, data=params)

    logger.info(url + ',' + res.text)

    return json.loads(res.text)

def bot_check_login(params):
    try:
        result = wechat_request('/bot_check_login', params)
    except:
        result = {'login': '0', 'desc': '请稍后再试'}
    return result

def bot_refresh_uuid(params):
    result = wechat_request('/bot_refresh_uuid', params)
    return result

def bot_notice(params):
    result = wechat_request('/bot_notice', params)
    return result


def bot_logout(params):
    result = wechat_request('/bot_logout', params)
    return result

def bot_wechat_bind(params):
    result = wechat_request('/bot_wechat_bind', params)
    return result

def bot_wechat_bind_manager(params):
    result = wechat_request('/bot_wechat_bind_manager', params)
    return result

def bot_wechat_friends(params):
    result = wechat_request('/bot_wechat_friends', params)
    return result

