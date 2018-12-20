#coding=utf-8
from . import wechatManager
from django.conf import settings
import json


def bot_key_check(key):
    if key == settings.BOT_KEY:
        return True
    else:
        return False

def bot_check_login(params):
    try:
        key = params["key"]
        club_name = params["name"]
        if not bot_key_check(key):
            return {'msg':'key error'}

        bot = wechatManager.wechatInstance.new_instance(club_name)
        wx_login = bot.is_login()
        return {'login': wx_login}
    except:
        return {'result': 4}