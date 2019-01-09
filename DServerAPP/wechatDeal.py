#coding=utf-8
from . import wechatManager
import json
import traceback
from .models import Clubs, Manager, Player
import time
import _thread

def bot_check_login(params):
    try:
        club_name = params["name"]

        bot = wechatManager.wechatInstance.new_instance(club_name)
        wx_login, desc = bot.get_login_status()
        return {'login': wx_login, 'desc': desc}
    except:
        return {'result': 4}

def bot_refresh_uuid(params):
    result = {'wx_login':True, 'uuid': ''}
    try:
        # 页面轮询机制
        club_name = params["name"]
        bot = wechatManager.wechatInstance.new_instance(club_name)
        wx_login, desc = bot.get_login_status()
        if not wx_login:
            bot.refresh_uuid()
            _thread.start_new_thread(bot.check_login)
            result["wx_login"] = False
        return
    except:
        traceback.print_exc()
        result["wx_login"] = False
        result["result"] = 4

    result["uuid"] = bot.get_uuid()
    return result


def bot_notice(params):
    try:
        club_name = params["name"]
        to_manager = params.get("manager", False)
        msg = params["msg"]
        player_id = int(params["player_id"])

        club = Clubs.objects.get(user_name=club_name)

        bot = wechatManager.wechatInstance.new_instance(club.user_name)
        wx_login = bot.is_login()
        if not wx_login:
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
        club_name = params["name"]

        bot = wechatManager.wechatInstance.new_instance(club_name)
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
        nick_name = params['nick_name']
        wechat_nick_name = params['wechat_nick_name']

        club = Clubs.objects.get(user_name=club_name)

        bot = wechatManager.wechatInstance.new_instance(club.user_name)
        wx_login = bot.is_login()
        if not wx_login:
            return {'result': 2}

        code, msg = bot.set_alias(user_name, nick_name)
        if code == 0:
            player = Player.objects.get(id=player_id)
            if player.club_id != club.uuid:
                return {'result': 1}
            player.nick_name = nick_name
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

        bot = wechatManager.wechatInstance.new_instance(club.user_name)
        wx_login = bot.is_login()
        if not wx_login:
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
        club_name = params["name"]
        nick_name = params['nick_name']
        wechat_nick_name = params['wechat_nick_name']
        club = Clubs.objects.get(user_name=club_name)

        bot = wechatManager.wechatInstance.new_instance(club.user_name)
        wx_login = bot.is_login()
        if not wx_login:
            return {'result': 2}

        list_ = bot.search_friends(wechat_nick_name, nick_name)

        return {'result': 0, 'list':list_}
    except:
        traceback.print_exc()
        return {'result': 4}
