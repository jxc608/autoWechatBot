#coding=utf-8
from . import wechatManager
import json
import traceback
from .models import Clubs, Manager, Player

import threading
import time
import inspect
import ctypes
import logging

logger = logging.getLogger(__name__)

_list = {}

def bot_check_login(params):
    wid = params["wid"]
    bot = wechatManager.wechatInstance.new_instance(wid)

    wx_login, desc = bot.get_login_status()
    return {'login': wx_login, 'desc': desc, 'uuid': bot.get_uuid()}

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


def bot_refresh_uuid(params):
    result = {}

    wid = params["wid"]
    bot = wechatManager.wechatInstance.new_instance(wid)
    wx_login, desc = bot.get_login_status()
    if not wx_login == '200':
        if _list.get(wid, None):
            stop_thread(_list[wid])
            bot = wechatManager.wechatInstance.new_instance(wid)
            logger.info("recreate bot: %s" % wid)

        bot.refresh_uuid()

        t1 = threading.Thread(target=bot.check_login, args=())
        _list[wid] = t1
        t1.start()

    result["uuid"] = bot.get_uuid()
    return result

def bot_notice(params):
    try:
        club_name = params["name"]
        to_manager = params.get("manager", False)
        msg = params["msg"]
        player_id = int(params["player_id"])

        club = Clubs.objects.get(user_name=club_name)
        wid = params['wid']
        bot = wechatManager.wechatInstance.new_instance(wid)
        wx_login, desc = bot.get_login_status()
        if wx_login != '200':
            return json.dumps({'result': 2})

        if to_manager:
            for manager in Manager.objects.filter(club=club):
                bot.sendByRemarkName(msg=msg, remarkName=manager.nick_name)
        else:
            player = Player.objects.get(id=player_id)
            if not player.is_bind:
                return {'result': 3}
            bot.sendByRemarkName(msg=msg, remarkName=player.nick_name)
        return {'result': 0}
    except:
        traceback.print_exc()
        return {'result': 4}


def bot_logout(params):
    try:
        wid = params["wid"]

        bot = wechatManager.wechatInstance.new_instance(wid)
        bot.logout()
        return {'result': True}
    except:
        traceback.print_exc()
        return {'result': 4}

def bot_wechat_bind(params):
    try:
        club_name = params["name"]
        player_id = int(params["id"])
        user_name = params['user_name']
        remark_name = params['nick_name']
        wechat_nick_name = params['wechat_nick_name']

        club = Clubs.objects.get(user_name=club_name)
        wid = params['wid']
        bot = wechatManager.wechatInstance.new_instance(wid)
        wx_login, desc = bot.get_login_status()
        if wx_login != '200':
            return {'result': 2, 'msg': desc}

        code, msg = bot.set_alias(user_name, remark_name)
        if code == 0:
            player = Player.objects.get(id=player_id)
            if player.club_id != club.uuid:
                return {'result': 1}
            player.nick_name = remark_name
            player.wechat_nick_name = wechat_nick_name
            player.is_bind = 1
            player.save()
            return {'result': 0}
        else:
            return {'result': 3, 'msg':msg}
    except:
        traceback.print_exc()
        return {'result': 4}

def bot_wechat_bind_manager(params):
    try:
        club_name = params["name"]
        user_name = params['user_name']
        nick_name = params['nick_name']
        wechat_nick_name = params['wechat_nick_name']

        club = Clubs.objects.get(user_name=club_name)
        wid = params['wid']
        bot = wechatManager.wechatInstance.new_instance(wid)
        wx_login, desc = bot.get_login_status()
        if wx_login != '200':
            return {'result': 2}

        code, msg = bot.set_alias(user_name, nick_name)
        if code == 0:
            manager = Manager(wechat_nick_name=wechat_nick_name, nick_name=nick_name, club=club, create_time=int(time.time()))
            manager.save()
            return {'result': 0}
        else:
            return {'result': 3, 'msg':msg}
    except:
        traceback.print_exc()
        return {'result': 4}

def bot_wechat_friends(params):
    try:
        wid = params["wid"]
        nick_name = params['nick_name']
        # wechat_nick_name = params['wechat_nick_name']

        bot = wechatManager.wechatInstance.new_instance(wid)
        wx_login, desc = bot.get_login_status()
        if wx_login != '200':
            return {'result': 2}

        list_ = bot.search_friends(nick_name)

        return {'result': 0, 'list':list_}
    except:
        traceback.print_exc()
        return {'result': 4}
