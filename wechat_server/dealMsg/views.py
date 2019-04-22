#coding=utf-8
from . import wechatManager
from . import statistics
import traceback
from DServerAPP.models import Clubs, Manager, Player
from django.http import JsonResponse
from django.conf import settings

import time
import logging
import json

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
    try:
        club_name = request.GET.get('name')
        to_manager = request.GET.get("manager", False)
        lastScore = request.GET.get('lastScore')
        chgScore = request.GET.get('chgScore')
        player_id = int(request.GET.get('player_id'))
        player = Player.objects.get(id=player_id)
        club = Clubs.objects.get(user_name=club_name)
        wid = request.GET.get('wid')
        mode = settings.WECHAT_MODE_ONLINE
        bot = wechatManager.wechatInstance.new_instance(wid)
        bot.club = club

        if club.appid:
            mode = settings.WECHAT_MODE_SERVICE
            tmid = settings.WECHAT_TEMPLATE_SCORE_ADD
            keyword1 = '游戏上分'
            if chgScore < 0:
                keyword1 = '游戏下分'
                tmid = settings.WECHAT_TEMPLATE_SCORE_MINUS
            alert_msg = {'first': '%s，上次积分' % (player.nick_name, lastScore), 'keyword1': keyword1, 'keyword2': chgScore,
                         'keyword3': player.current_score, 'remark': '感谢您的参与。', 'templateid': tmid}
        else:
            if not able_dict[0]:
                return JsonResponse({'result': 2})

            wx_login, desc = bot.check_login_status()
            if wx_login != '200':
                return JsonResponse({'result': 2})

            alert_msg = '%s %s\n' % (player.nick_name, op)
            alert_msg += '上次积分:%s\n' % lastScore
            alert_msg += '本次%s:%s\n' % (op, chgScore)
            alert_msg += '当前余分:%s\n' % player.current_score

        if to_manager:
            for manager in Manager.objects.filter(club=club):
                online_user = ''
                if mode == settings.WECHAT_MODE_ONLINE:
                    f = bot.getWechatUserByRemarkName(remarkName=manager.nick_name)
                    online_user = f['UserName']
                bot.send_mode_msg(mode, content=alert_msg, tm_param=alert_msg, online_user=online_user, openid=manager.openid, is_template=True)
            return JsonResponse({'result': 0})
        else:
            if not player.is_bind:
                return JsonResponse({'result': 3})
            online_user = ''
            if mode == settings.WECHAT_MODE_ONLINE:
                f = bot.getWechatUserByRemarkName(remarkName=player.nick_name)
                online_user = f['UserName']
            bot.send_mode_msg(mode, content=alert_msg, tm_param=alert_msg, openid=player.openid, online_user=online_user, is_template=True)
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


def check_club_status(request):
    result = {'response': 'ok'}
    appid = request.POST.get('appid', '')
    if not appid:
        result.update(response='fail', error='appid is empty: %s' % appid)
    else:
        try:
            club = Clubs.objects.get(appid=appid)
            if club.expired_time < time.time():
                result.update(response='fail', error=u'您的cdkey已过期, appid: %s' % appid)
        except:
            error = u'俱乐部未绑定服务号： %s' % appid
            logger.error(error)
            result.update(response='fail', error=error)

    return JsonResponse(result)

def orc_add_one(request):
    result = {'response': 'ok'}
    appid = request.POST.get('appid', '')
    if not appid:
        result.update(response='fail', error='appid is empty: %s' % appid)
    else:
        try:
            club = Clubs.objects.get(appid=appid)
            if club.expired_time < time.time():
                error = '俱乐部已过期： %s， 请与管理员确认' % club.user_name
                logger.error(error)
                result.update(response='fail', error=error)
            else:
                statistics.addClubOrcCount(club)
        except:
            error = u'俱乐部未绑定服务号： %s' % appid
            logger.error(error)
            result.update(response='fail', error=error)

    return JsonResponse(result)

def deal_img_data(request):
    result = {'response': 'ok'}
    body = request.body
    body = json.loads(body)
    appid = body.get('appid', '')
    mediaId = body.get('mediaid', '')
    content = body.get('content', '')
    fromuser = body.get('fromuser', '')
    try:
        club = Clubs.objects.get(appid=appid)

    except:
        error = u'俱乐部未绑定服务号： %s' % appid
        logger.error(error)
        result.update(response='fail', error=error)
    try:
        if club:
            if club.expired_time < time.time():
                error = '俱乐部已过期： %s， 请与管理员确认' % club.user_name
                logger.error(error)
                result.update(response='fail', error=error)
            else:
                bot = wechatManager.wechatInstance.new_instance(club.user_name)
                bot.deal_img_data(settings.WECHAT_MODE_SERVICE, content, mediaId=mediaId, fromuser=fromuser, club=club)
    except:
        traceback.print_exc()
        error = "发送微信消息出错"
        result.update(response='fail', error=error)

    return JsonResponse(result)

