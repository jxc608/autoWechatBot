#coding=utf-8
from . import wechatManager
import traceback
from DServerAPP.models import Clubs, Manager, Player
from django.http import JsonResponse

import time
import logging

logger = logging.getLogger(__name__)

able_dict = [True]

def logout_all(request):
    able_dict[0] = False
    wechatManager.wechatInstance.logoutAll()
    logger.info("command: logout_all")
    return JsonResponse({ 'result': 'ok' })

def bot_check_login(request):
    if not able_dict[0]:
        return JsonResponse({'login': '0', 'desc': ''})

    wid = request.GET.get('wid')
    bot = wechatManager.wechatInstance.new_instance(wid)
    wx_login, desc = bot.check_login_status()

    return JsonResponse({'login': wx_login, 'desc': desc})

def bot_refresh_uuid(request):
    if not able_dict[0]:
        return JsonResponse({ 'uuid': '' })

    result = {}
    wid = request.GET.get('wid')
    bot = wechatManager.wechatInstance.new_instance(wid)
    result["uuid"] = bot.refresh_uuid()

    return JsonResponse(result)

def bot_notice(request):
    if not able_dict[0]:
        return JsonResponse({'result': 2})
    try:
        club_name = request.GET.get('name')
        to_manager = request.GET.get("manager", False)
        msg = request.GET.get('msg')
        player_id = int(request.GET.get('player_id'))

        club = Clubs.objects.get(user_name=club_name)
        wid = request.GET.get('wid')
        bot = wechatManager.wechatInstance.new_instance(wid)
        wx_login, desc = bot.check_login_status()
        if wx_login != '200':
            return JsonResponse({'result': 2})

        if to_manager:
            for manager in Manager.objects.filter(club=club):
                bot.sendByRemarkName(msg=msg, remarkName=manager.nick_name)
            return JsonResponse({'result': 0})
        else:
            player = Player.objects.get(id=player_id)
            if not player.is_bind:
                return JsonResponse({'result': 3})
            bot.sendByRemarkName(msg=msg, remarkName=player.nick_name)
            return JsonResponse({'result': 0})
    except:
        traceback.print_exc()
        return JsonResponse({'result': 4})


def bot_logout(request):
    if not able_dict[0]:
        return JsonResponse({'result': True})
    try:
        wid = request.GET.get('wid')

        bot = wechatManager.wechatInstance.new_instance(wid)
        bot.logout()
        return JsonResponse({'result': True})
    except:
        traceback.print_exc()
        return JsonResponse({'result': 4})

def bot_wechat_bind(request):
    if not able_dict[0]:
        return JsonResponse({'result': 2})
    try:
        club_name = request.GET.get('name')
        player_id = int(request.GET.get('id'))
        user_name = request.GET.get('user_name')
        remark_name = request.GET.get('nick_name')
        wechat_nick_name = request.GET.get('wechat_nick_name')

        club = Clubs.objects.get(user_name=club_name)
        wid = request.GET.get('wid')
        bot = wechatManager.wechatInstance.new_instance(wid)
        wx_login, desc = bot.check_login_status()
        if wx_login != '200':
            return JsonResponse({'result': 2, 'msg': desc})

        code, msg = bot.set_alias(user_name, remark_name)
        if code == 0:
            player = Player.objects.get(id=player_id)
            if player.club_id != club.uuid:
                return JsonResponse({'result': 1})
            player.nick_name = remark_name
            player.wechat_nick_name = wechat_nick_name
            player.is_bind = 1
            player.save()
            return JsonResponse({'result': 0})
        else:
            return JsonResponse({'result': 3, 'msg':msg})
    except:
        traceback.print_exc()
        return JsonResponse({'result': 4})

def bot_wechat_bind_manager(request):
    if not able_dict[0]:
        return JsonResponse({'result': 2})
    try:
        club_name = request.GET.get('name')
        user_name = request.GET.get('user_name')
        nick_name = request.GET.get('nick_name')
        wechat_nick_name = request.GET.get('wechat_nick_name')

        club = Clubs.objects.get(user_name=club_name)
        wid = request.GET.get('wid')
        bot = wechatManager.wechatInstance.new_instance(wid)
        wx_login, desc = bot.check_login_status()
        if wx_login != '200':
            return JsonResponse({'result': 2})

        code, msg = bot.set_alias(user_name, nick_name)
        if code == 0:
            manager = Manager(wechat_nick_name=wechat_nick_name, nick_name=nick_name, club=club, create_time=int(time.time()))
            manager.save()
            return JsonResponse({'result': 0})
        else:
            return JsonResponse({'result': 3, 'msg':msg})
    except:
        traceback.print_exc()
        return JsonResponse({'result': 4})

def bot_wechat_friends(request):
    if not able_dict[0]:
        return JsonResponse({'result': 2})
    try:
        wid = request.GET.get('wid')
        nick_name = request.GET.get('nick_name')

        bot = wechatManager.wechatInstance.new_instance(wid)
        wx_login, desc = bot.check_login_status()
        if wx_login != '200':
            return JsonResponse({'result': 2})

        list_ = bot.search_friends(nick_name)

        return JsonResponse({'result': 0, 'list':list_})
    except:
        traceback.print_exc()
        return JsonResponse({'result': 4})
