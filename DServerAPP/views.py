# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
import uuid
from . import messageType
from .utils import is_number
import time,datetime,json
from django.db import connection
from django.conf import settings
from django.db.models import Sum
import xlwt
import io, math
from . import wechatDeal
from functools import wraps
import logging

logger = logging.getLogger(__name__)

def timestamp2string(timeStamp):
  try:
    timeArray = time.localtime(timeStamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
  except Exception as e:
    logger.error(e)
    return ''

def get_bot_param(request):
    params = {}
    params["name"] = request.session['club']
    params["key"] = request.GET.get("key"),
    params['wid'] = request.session['wid']

    return params


def wx_logout(request):
    params = get_bot_param(request)
    bot_info = wechatDeal.bot_logout(params)
    return HttpResponse(json.dumps(bot_info), content_type="application/json")

def wechat_friends(request):
    nick_name = request.POST.get('nick_name')
    params = {
                'name':request.session['club'],
                'nick_name':nick_name,
                'wid': request.session['wid'],
             }
    bot_info = wechatDeal.bot_wechat_friends(params)

    return HttpResponse(json.dumps(bot_info), content_type="application/json")

def wechat_bind(request):
    player_id = int(request.POST.get('id'))
    user_name = request.POST.get('user_name')
    nick_name = request.POST.get('remark_name')
    wechat_nick_name = request.POST.get('wechat_nick_name')

    params = {
                'name':request.session['club'],
                'id':player_id,
                'nick_name':nick_name,
                'wechat_nick_name':wechat_nick_name,
                'user_name':user_name,
                'wid': request.session['wid'],
             }
    bot_info = wechatDeal.bot_wechat_bind(params)


    return HttpResponse(json.dumps(bot_info), content_type="application/json")


def check_sys_login(f):
    wraps(f)

    def inner(request, *arg, **kwargs):
        if not request.session.get('login'):
            return HttpResponseRedirect('/login')
        else:
            return f(request, *arg, **kwargs)
    return inner

@check_sys_login
def check_wx_login(request):
    params = get_bot_param(request)
    bot_info = wechatDeal.bot_check_login(params)
    # logger.info(bot_info)
    return HttpResponse(json.dumps(bot_info), content_type="application/json")

@check_sys_login
def refresh_uuid(request):
    params = get_bot_param(request)
    try:
        bot_info = wechatDeal.bot_refresh_uuid(params)
    except:
        bot_info = {'uuid': ''}
    # logger.info(bot_info)
    return HttpResponse(json.dumps({'uuid': bot_info['uuid']}), content_type="application/json")

@check_sys_login
def index(request):
    club = Clubs.objects.get(user_name=request.session['club'])
    club.expired = False
    if club.expired_time < time.time():
        club.expired_time_desc = '已失效'
        club.expired = True
        bot_info = {"login": '488', "uuid": ""}
    else:
        timeArray = time.localtime(club.expired_time)
        club.expired_time_desc = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        params = get_bot_param(request)
        # 第一次不用设置二维码，页面统一刷新uuid来获取
        bot_info = {"login": '0', "uuid": ""}
        # try:
        #     bot_info = wechatDeal.bot_check_login(params)
        # except:
        #     bot_info = {"login": '0', "uuid": ""}

    is_admin = False
    if club.user_name == '18811333964':
        is_admin = True
    return render(request, 'DServerAPP/index.html', {'club':club, 'wx_login':bot_info['login'], 'is_admin':is_admin})

def login(request):
    return render(request, 'DServerAPP/login.html')

def logout(request):
    try:
        del request.session['login']
        del request.session['club']
        del request.session['wid']
    except:
        pass
    return HttpResponseRedirect('/login')

def registerPage(request):
    return render(request, 'DServerAPP/register.html')

def register(request):
    username=request.POST.get('username','')
    password=request.POST.get('password','')
    cpassword=request.POST.get('cpassword','')
    password2 = request.POST.get("password2")
    result = {
        "username": username,
        "password": password,
        "cpassword": cpassword,
        "password2": password2
    }
    err = False
    if username == "":
        result["account"] = 1
        result["acct"] = "账号为空"
        err = True
    elif password == '':
        result["pwd"] = 1
        result["pwct"] = "密码为空"
        err = True
    elif  password != cpassword:
        result["pwd"] = 1
        result["pwct"] = "两次密码不一致"
        err = True
    elif password2 == "":
        result["pwd"] = 1
        result["pwct"] = "二级密码为空"
        err = True
    if err:
        return render(request, 'DServerAPP/register.html', result)

    if Clubs.objects.filter(user_name=username).count() > 0:
        return render(request, 'DServerAPP/register.html', {"account": 1, "acct": "账号已注册"})
    else:
        password = request.POST.get('password', '')
        expired = time.time() + 3600 * 3

        club = Clubs(uuid=uuid.uuid1(), user_name=username, password=password, password2=password2,
                     expired_time=expired, cost_mode=0, cost_param='')
        club.save()
        return render(request, 'DServerAPP/register.html', {"account": 2, "acct": "注册成功！"})

def change_passwd(request):
    old_passwd = request.POST.get('old_passwd','')
    new_passwd = request.POST.get('new_passwd','')

    club = Clubs.objects.get(user_name=request.session['club'])
    if old_passwd != club.password:
        return HttpResponse(json.dumps({'result':1}), content_type="application/json")
    club.password = new_passwd
    club.save()
    return HttpResponse(json.dumps({'result':0}), content_type="application/json")


def login_password(request):
    username=request.POST.get('username','')
    password=request.POST.get('password','')
    if username == '':
        return render(request, 'DServerAPP/login.html', {"account": 1, "acct":"账号为空" })
    elif password == '':
        return render(request, 'DServerAPP/login.html', {"pwd": 1, "pwct": "密码为空"})
    else:
        try:
            club = Clubs.objects.get(user_name=username)
            if club.password != password:
                return render(request, 'DServerAPP/login.html', {"pwd": 1, "pwct": "密码错误"})
            else:
                request.session['login'] = True
                request.session['club'] = username

                if request.META.get('HTTP_X_FORWARDED_FOR'):
                    ip = request.META['HTTP_X_FORWARDED_FOR']
                else:
                    ip = request.META['REMOTE_ADDR']

                request.session['wid'] = "%s__,__%s" % (username, ip)
                #登录成功之后，渲染页面
                return HttpResponseRedirect('/')
        except Clubs.DoesNotExist:
            return render(request, 'DServerAPP/login.html', {"pwd": 1, "pwct": "账号不存在"})


# def login_smscode(request):
#     username=request.POST.get('username','')
#     smscode=request.POST.get('smscode','')
#     return HttpResponse('username='+username+"&password="+password)

def add_time(request):
    username=request.session['club']
    cdkey=request.POST.get('cdkey')
    try:
        keyInstance = Cdkey.objects.get(cdkey=cdkey)
        if keyInstance.status == 1:
            return HttpResponse(messageType.createMessage('success', messageType.CDKEY_USED, 'the cdkey used'))
        time_add = 0
        if keyInstance.key_type == 1:
            time_add = 3600 * 24
        elif keyInstance.key_type == 2:
            time_add = 3600 * 24 * 7
        elif keyInstance.key_type == 3:
            time_add = 3600 * 24 * 30
    except Cdkey.DoesNotExist:
        return HttpResponse(messageType.createMessage('success', messageType.CDKEY_NOT_EXIST, 'the cdkey not exist'))

    try:
        clubInstance = Clubs.objects.get(user_name=username)
        if clubInstance.expired_time < time.time():
            clubInstance.expired_time = time.time() + time_add
        else:
            clubInstance.expired_time += time_add
        clubInstance.save()
        keyInstance.status = 1
        keyInstance.use_time = datetime.datetime.now()
        keyInstance.club = clubInstance
        keyInstance.save()
        return HttpResponse(messageType.createMessage('success', messageType.SUCCESS, 'add time succeed'))
    except Clubs.DoesNotExist:
        return HttpResponse(messageType.createMessage('success', messageType.CLUB_NOT_EXIST, 'the club not exist'))

def create_cdkey(request):
    if request.session['club'] != '18811333964':
        return

    key_type = int(request.POST.get('key_type'))
    num = int(request.POST.get('num'))
    content = []
    for x in range(0, num):
        key = Cdkey()
        key.cdkey = str(uuid.uuid1())[:8]
        key.key_type = key_type
        key.status = 0
        key.create_time = int(time.time())
        key.save()
        content.append(key.cdkey)
    return HttpResponse(json.dumps({'result': True, 'content': content}), content_type="application/json")

def get_cdkey(request):
    key_type = int(request.POST.get('key_type'))
    num = int(request.POST.get('num'))
    keys = Cdkey.objects.filter(status=0, key_type=key_type)[:num]
    result = []
    for key in keys:
        result.append(key.cdkey)
    return HttpResponse(json.dumps({'result': result}), content_type="application/json")

@check_sys_login
def room_data(request):
    day = datetime.datetime.now().strftime('%Y-%m-%d')
    if request.GET.get('date'):
        day = request.GET.get('date')
    orderby = request.GET.get('order', 'round')

    club = Clubs.objects.get(user_name=request.session['club'])
    rooms = HistoryGame.objects.filter(club=club, refresh_time__startswith=day)
    total_cost = 0
    total_score = 0
    total_round = 0
    total_profit = 0
    for room in rooms:
        total_cost += room.cost
        # total_score += room.score
        total_round += room.round_number
        # total_profit += room.score - room.cost
        pd = json.loads(room.player_data)
        logger.info(pd[0])
        room.score = int(pd[0]['score'])

    if orderby == 'cost':
        rooms = sorted(rooms, key=lambda rooms : rooms.cost, reverse=True)
    elif orderby == 'score':
        rooms = sorted(rooms, key=lambda rooms : rooms.score, reverse=True)
    elif orderby == 'round':
        rooms = sorted(rooms, key=lambda rooms : rooms.round_number, reverse=True)
    total = len(rooms)

    return render(request, 'DServerAPP/room_data.html', {'rooms':rooms, 'total':total, 'total_cost':total_cost, 'total_score':total_score, 'total_round':total_round, 'total_profit':total_profit, 'day':day})

def clear_room_data(request):
    second_password = request.POST.get("second_password", '')
    club = Clubs.objects.get(user_name=request.session['club'])
    result = {'result': 0}
    if second_password != club.password2:
        result["result"] = 1
        result["errmsg"] = "二级密码不正确"
    else:
        day = datetime.datetime.now().strftime('%Y-%m-%d')
        if request.POST.get('date'):
            day = request.POST.get('date')

        club = Clubs.objects.get(user_name=request.session['club'])
        rooms = HistoryGame.objects.filter(club=club, refresh_time__startswith=day)
        for room in rooms:
            if room.cost == 0:
                continue
            hc = HistoryGameClearCost(history_id=room.id,cost=room.cost)
            hc.save()
            room.cost = 0
            room.save()

    return HttpResponse(json.dumps(result), content_type="application/json")

@check_sys_login
def player_room_data(request):
    club = Clubs.objects.get(user_name=request.session['club'])
    day = datetime.datetime.now().strftime('%Y-%m-%d')
    if request.GET.get('date'):
        day = request.GET.get('date')
    orderby = request.GET.get('order', 'round')
    players = Player.objects.filter(club=club, is_del=0).order_by('-current_score', '-history_profit')

    list_ = []
    for player in players:
        player.gameids = GameID.objects.filter(player_id=player.id)
        player.total_round = Score.objects.filter(player_id=player.id, refresh_time__startswith=day).count()
        if player.total_round == 0:
            continue
        player.total_cost = Score.objects.filter(player_id=player.id, refresh_time__startswith=day).aggregate(Sum('cost'))['cost__sum']
        if player.total_cost == None:
            player.total_cost = 0
        player.total_score = Score.objects.filter(player_id=player.id, refresh_time__startswith=day).aggregate(Sum('score'))['score__sum']
        if player.total_score == None:
            player.total_score = 0
        player.total_host = Score.objects.filter(player_id=player.id, refresh_time__startswith=day).aggregate(Sum('is_host'))['is_host__sum']
        if player.total_host == None:
            player.total_host = 0
        list_.append(player)
    if orderby == 'round':
        list_ = sorted(list_, key=lambda list_ : list_.total_round, reverse=True)
    elif orderby == 'host':
        list_ = sorted(list_, key=lambda list_ : list_.total_host, reverse=True)
    elif orderby == 'score':
        list_ = sorted(list_, key=lambda list_ : list_.total_score, reverse=True)
    elif orderby == 'cost':
        list_ = sorted(list_, key=lambda list_ : list_.total_cost, reverse=True)
    return render(request, 'DServerAPP/player_room_data.html', {'players':list_,'day':day})

@check_sys_login
def player_data(request):
    nickname_search = request.GET.get('nickname','')
    gameid_search = request.GET.get('gameid', '')
    pageSize = int(request.GET.get('pageSize', 50))
    pageIndex = int(request.GET.get('pageIndex', 1))

    club = Clubs.objects.get(user_name=request.session['club'])
    if gameid_search:
        gameids = GameID.objects.filter(gameid=gameid_search, club=club).values("player_id").distinct()
        if gameids.count() == 0:
            return render(request, 'DServerAPP/player_data.html', {'club':club, 'players':[], 'total':0, 'nickname':nickname_search, 'gameid':gameid_search})
    if gameid_search:
        for gameid in gameids:
            players = Player.objects.filter(club=club, is_del=0, id=gameid['player_id']).order_by('-current_score')
            if players:
                break
    elif nickname_search:
        players = Player.objects.filter(club=club, is_del=0, nick_name__contains=nickname_search).order_by('-current_score')
    else:
        players = Player.objects.filter(club=club, is_del=0).order_by('-current_score', '-history_profit')

    total = players.count()
    start = (pageIndex - 1) * pageSize
    end = pageIndex * pageSize
    totalPage = math.ceil(float(total) / pageSize)
    players = players[start:end]
    for player in players:
        gameids = GameID.objects.filter(player_id=player.id)
        player.gameids = gameids

    return render(request, 'DServerAPP/player_data.html', {'club':club, 'players':players, 'total':total, 'totalPage': totalPage, 'pageSize': pageSize, 'pageIndex': pageIndex, 'nickname':nickname_search, 'gameid':gameid_search})

@check_sys_login
def player_stat(request):
    nickname_search = request.GET.get('nickname','')
    gameid_search = request.GET.get('gameid', '')
    club = Clubs.objects.get(user_name=request.session['club'])

    if gameid_search:
        search_gameids = GameID.objects.filter(gameid=gameid_search, club=club).values("player_id").distinct()
        if search_gameids.count() == 0:
            return render(request, 'DServerAPP/player_data.html', {'club':club, 'players':[], 'total':0, 'nickname':nickname_search, 'gameid':gameid_search})
    if gameid_search:
        for gameid in search_gameids:
            players_cost = Player.objects.filter(club=club, is_del=0, id=gameid['player_id']).order_by('-history_cost')
            if players_cost:
                break
    elif nickname_search:
        players_cost = Player.objects.filter(club=club, is_del=0, nick_name__contains=nickname_search).order_by('-history_cost')
    else:
        players_cost = Player.objects.filter(club=club, is_del=0).order_by('-history_cost')

    for player in players_cost:
        gameids = GameID.objects.filter(player_id=player.id)
        player.gameids = gameids

    if gameid_search:
        for gameid in search_gameids:
            players_profit = Player.objects.filter(club=club, is_del=0, id=gameid['player_id']).order_by('-history_profit')
            if players_profit:
                break
    elif nickname_search:
        players_profit = Player.objects.filter(club=club, is_del=0, nick_name__contains=nickname_search).order_by('-history_profit')
    else:
        players_profit = Player.objects.filter(club=club, is_del=0).order_by('-history_profit')

    for player in players_profit:
        gameids = GameID.objects.filter(player_id=player.id)
        player.gameids = gameids
    total = len(players_profit)

    list_ = []
    for index, player in enumerate(players_cost):
        list_.append(
            {
                'cost':player,
                'profit':players_profit[index]
            }
        )
    return render(request, 'DServerAPP/player_stat.html', {'club':club, 'list':list_, 'total':total, 'nickname':nickname_search, 'gameid':gameid_search})

def clear_player_stat(request):
    second_password = request.POST.get("second_password", '')
    club = Clubs.objects.get(user_name=request.session['club'])
    result = {'result': 0}
    if second_password != club.password2:
        result["result"] = 1
        result["errmsg"] = "二级密码不正确"
    else:
        nickname_search = request.POST.get('nickname','')
        gameid_search = request.POST.get('gameid', '')

        if gameid_search:
            search_gameids = GameID.objects.filter(gameid=gameid_search, club=club).values("player_id").distinct()
            if search_gameids.count() == 0:
                return render(request, 'DServerAPP/player_data.html', {'club':club, 'players':[], 'total':0, 'nickname':nickname_search, 'gameid':gameid_search})
        if gameid_search:
            for gameid in search_gameids:
                players_cost = Player.objects.filter(club=club, is_del=0, id=gameid['player_id']).order_by('-history_cost')
                if players_cost:
                    break
        elif nickname_search:
            players_cost = Player.objects.filter(club=club, is_del=0, nick_name__contains=nickname_search).order_by('-history_cost')
        else:
            players_cost = Player.objects.filter(club=club, is_del=0).order_by('-history_cost')

        for player in players_cost:
            if player.history_cost == 0:
                continue
            pc = PlayerClearCost(player_id=player.id, history_cost=player.history_cost)
            pc.save()
            player.history_cost = 0
            player.save()
    return HttpResponse(json.dumps(result), content_type="application/json")

def add_manager(request):
    user_name = request.POST.get('user_name')
    nick_name = request.POST.get('nick_name')
    wechat_nick_name = request.POST.get('wechat_nick_name')
    params = {
        'name': request.session['club'],
        'nick_name': nick_name,
        'wechat_nick_name': wechat_nick_name,
        'user_name': user_name,
        'wid': request.session['wid'],
    }
    bot_info = wechatDeal.bot_wechat_bind_manager(params)

    return HttpResponse(json.dumps(bot_info), content_type="application/json")

def del_manager(request):
    manager_id = int(request.POST.get('id'))
    club = Clubs.objects.get(user_name=request.session['club'])

    manager = None
    try:
        manager = Manager.objects.get(id=manager_id, club=club)
        manager.delete()
    except manager.DoesNotExist:
        return HttpResponse(json.dumps({'result': 1}), content_type="application/json")

    return HttpResponse(json.dumps({'result': 0}), content_type="application/json")

def add_player(request):
    nickname = request.POST.get('nickname')
    gameid = int(request.POST.get('gameid'))

    club = Clubs.objects.get(user_name=request.session['club'])
    if Player.objects.filter(nick_name=nickname, club=club, is_del=0).count() > 0:
        return HttpResponse(json.dumps({'result': 1}), content_type="application/json")

    player = Player(wechat_nick_name='tempUser', nick_name=nickname, club=club, current_score=0, history_profit=0)
    player.save()
    gameid = GameID(player=player, club=club, gameid=gameid, game_nick_name=nickname)
    gameid.save()

    return HttpResponse(json.dumps({'result': 0}), content_type="application/json")

def del_player(request):
    second_password = request.POST.get("second_password")
    club = Clubs.objects.get(user_name=request.session['club'])
    result = {'result': 0}
    if second_password != club.password2:
        result["result"] = 1
        result["errmsg"] = "二级密码不正确"
    else:
        player_id = int(request.POST.get('id'))
        try:
            player = Player.objects.get(id=player_id, club=club)
            player.is_del = 1
            player.save()
        except Player.DoesNotExist:
            result["result"] = 2
            result["errmsg"] = "玩家不存在"

    return HttpResponse(json.dumps(result), content_type="application/json")

def add_gameid(request):
    # 对应，添加小号
    player_id = int(request.POST.get('id'))
    gameid = int(request.POST.get('gameid'))

    club = Clubs.objects.get(user_name=request.session['club'])
    result = {"result": 0}
    try:
        player = Player.objects.get(id=player_id, club=club, is_del=0)
        gameIDAry = GameID.objects.filter(gameid=gameid, club=club, player__is_del=0)
        # 每个club的每个gameid，对应的is_del为0的player，该只有一条
        if gameIDAry.count() > 1:
            result["result"] = 2
            result["errmsg"] = "游戏ID已添加到其他用户，请先从其他用户中删除！"
        elif gameIDAry.count() == 1:
            original_player = gameIDAry[0].player
            if original_player.id == player_id:
                result["result"] = 3
                result["errmsg"] = "已在该用户中"
            else:
                GameID.objects.filter(gameid=gameid, club=club, player__is_del=0).update(player_id=player.id)
                Score.objects.filter(player_id=original_player.id).update(player_id=player.id)
                ScoreChange.objects.filter(player_id=original_player.id).update(player_id=player.id)
                player.current_score += original_player.current_score
                player.history_profit += original_player.history_profit
                player.history_cost += original_player.history_cost
                player.today_hoster_number += original_player.today_hoster_number
                player.save()
                original_player.delete()
        else:
            gameid = GameID(player=player, club=club, gameid=gameid, game_nick_name=player.nick_name)
            gameid.save()

    except Player.DoesNotExist:
        result["result"] = 1
        result["errmsg"] = "用户不存在"

    return HttpResponse(json.dumps(result), content_type="application/json")

def del_gameid(request):
    second_password = request.POST.get("second_password")
    club = Clubs.objects.get(user_name=request.session['club'])
    result = {'result': 0}
    if second_password != club.password2:
        result["result"] = 1
        result["errmsg"] = "二级密码不正确"
    else:
        player_id = int(request.POST.get('id'))
        gameid = int(request.POST.get('gameid'))
        if Player.objects.filter(id=player_id, club=club).count() == 0:
            result["result"] = 1
            result["errmsg"] = "用户不存在"
        else:
            # 每个club的每个gameid，对应的is_del为0的player，该只有一条，就是下面的这一条
            GameID.objects.filter(player_id=player_id, gameid=gameid, club=club).delete()

    return HttpResponse(json.dumps(result), content_type="application/json")

def add_score(request):
    player_id = int(request.POST.get('id'))
    score = abs(int(request.POST.get('score')))
    notice = request.POST.get('notice') == 'true'

    club = Clubs.objects.get(user_name=request.session['club'])
    player = Player.objects.get(id=player_id)
    if player.club_id != club.uuid:
        return HttpResponse(json.dumps({'result': 1}), content_type="application/json")
    current_score = player.current_score
    player.current_score += score
    player.save()
    agent = request.ua.os
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']

    score_change = ScoreChange(player=player, score=score, agent=agent, ip=ip, create_time=int(time.time()))
    score_change.save()
    msg = player.nick_name+' 上分\n'
    msg+= '上次积分:%s\n' % current_score
    msg+= '本次上分:%s\n' % score
    msg+= '当前余分:%s\n' % player.current_score

    params = {
        'key': request.GET.get("key"),
        'name':club.user_name,
        'player_id':player_id,
        'msg':msg,
        'wid': request.session['wid'],
    }
    if notice:
        wechatDeal.bot_notice(params)
    params['manager'] = True
    wechatDeal.bot_notice(params)

    return HttpResponse(json.dumps({'result': 0, 'current_score':player.current_score}), content_type="application/json")

def minus_score(request):
    player_id = int(request.POST.get('id'))
    score = abs(int(request.POST.get('score')))
    notice = request.POST.get('notice') == 'true'

    club = Clubs.objects.get(user_name=request.session['club'])
    player = Player.objects.get(id=player_id)
    if player.club_id != club.uuid:
        return HttpResponse(json.dumps({'result': 1}), content_type="application/json")

    current_score = player.current_score
    player.current_score -= score
    player.save()
    agent = request.ua.os

    if request.META.get('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']

    score_change = ScoreChange(player=player, score=-score, agent=agent, ip=ip, create_time=int(time.time()))
    score_change.save()
    msg = player.nick_name+' 下分\n'
    msg+= '上次积分:%s\n' % current_score
    msg+= '本次下分:-%s\n' % score
    msg+= '当前余分:%s\n' % player.current_score
    params = {
        'key': request.GET.get("key"),
        'name': club.user_name,
        'player_id': player_id,
        'msg': msg,
        'wid': request.session['wid'],
    }
    if notice:
        wechatDeal.bot_notice(params)
    params['manager'] = True
    wechatDeal.bot_notice(params)

    return HttpResponse(json.dumps({'result': 0, 'current_score':player.current_score}), content_type="application/json")

def add_score_limit(request):
    player_id = int(request.POST.get('id'))
    score = abs(int(request.POST.get('score',0)))
    score_desc = request.POST.get('score_desc')

    club = Clubs.objects.get(user_name=request.session['club'])
    player = Player.objects.get(id=player_id)
    if player.club_id != club.uuid:
        return HttpResponse(json.dumps({'result': 1}), content_type="application/json")
    player.score_limit = score
    player.score_limit_desc = score_desc

    player.save()

    return HttpResponse(json.dumps({'result': 0, 'score_limit':player.score_limit}), content_type="application/json")

@check_sys_login
def score_change(request):
    nickname_search = request.GET.get('nickname','')
    gameid_search = request.GET.get('gameid', '')

    pageSize = int(request.GET.get('pageSize', 50))
    pageIndex = int(request.GET.get('pageIndex', 1))

    orderby = request.GET.get('order', 'round')
    club = Clubs.objects.get(user_name=request.session['club'])

    players = Player.objects.filter(club=club, is_del=0)
    if nickname_search:
        players = players.filter(nick_name__contains=nickname_search)
    if gameid_search:
        gamePlayers = GameID.objects.filter(gameid=gameid_search, club=club).values("player").distinct()
        players = players.filter(id__in=gamePlayers)

    total = players.count()
    start = (pageIndex - 1) * pageSize
    end = pageIndex * pageSize
    totalPage = math.ceil(float(total) / pageSize)

    for player in players:
        player.gameids = GameID.objects.filter(player_id=player.id)
        player.gameids_count = len(player.gameids)
        player.total_round = Score.objects.filter(player_id=player.id).count()
    if orderby == 'round':
        players = sorted(players, key=lambda players : players.total_round, reverse=True)
    else:
        players = sorted(players, key=lambda players : players.current_score, reverse=True)

    players = players[start:end]

    return render(request, 'DServerAPP/score_change.html', {'club':club, 'players':players, 'total':total, 'nickname':nickname_search, 'pageSize': pageSize, 'pageIndex': pageIndex, 'totalPage': totalPage, 'gameid':gameid_search})

@check_sys_login
def save_captain(request):
    code = 0
    errmsg = ""
    club = Clubs.objects.get(user_name=request.session['club'])
    id = request.POST.get("id", "")
    name = request.POST.get("name", "")
    if name == "":
        code = 1
        errmsg = "名字为空"
    elif id == "":
        cp = Captain(club=club, name=name)
        cp.save()
    else:
        try:
            cp = Captain.objects.get(id=int(id))
            cp.name = name
            cp.save()
        except:
            code = 2
            errmsg = "更新失败，请刷新后再试"

    result = {"result": code, "errmsg": errmsg}
    return HttpResponse(json.dumps(result), content_type="application/json")

@check_sys_login
def score_change_group(request):
    club = Clubs.objects.get(user_name=request.session['club'])
    date = request.GET.get("date", None)
    cp = request.GET.get("cp", "")
    pageSize = int(request.GET.get('pageSize', 3))
    pageIndex = int(request.GET.get('pageIndex', 1))
    introAry, total, totalPage = getDayGroup(club, date, cp, pageSize, pageIndex)
    qryType = "历史" if not date else "当日"
    return render(request, 'DServerAPP/score_change_group.html', {'club':club, 'introAry': introAry, 'totalPage': totalPage, 'pageSize': pageSize, 'pageIndex': pageIndex, 'total': total,"date": date, "cp": cp, "qryType": qryType})

def getDayGroup(club, date, captainName, pageSize, pageIndex):
    introducers = Captain.objects.filter(club=club)
    if captainName:
        introducers = introducers.filter(name__contains=captainName)

    total = introducers.count()
    start = (pageIndex - 1) * pageSize
    end = pageIndex * pageSize
    totalPage = math.ceil(float(total) / pageSize)
    introducers = introducers[start:end]
    introAry = []
    for introducer in introducers:
        introDict = {"intorducer": introducer}
        playerAry = []
        players = Player.objects.filter(introducer=introducer, is_del=0)
        allScore = 0
        allRound = 0
        allCost = 0
        for player in players:
            sc = Score.objects.filter(player=player)
            # scc = ScoreChange.objects.filter(player=player)
            if date:
                sc = sc.filter(create_time__startswith=date)
                # scc = scc.filter(create_time__startswith=date)
            cost = sc.aggregate(Sum('cost'))['cost__sum']
            cost = 0 if not cost else cost
            round = sc.count()
            sc = sc.aggregate(Sum('score'))['score__sum']
            sc = 0 if not sc else sc
            # scc = scc.aggregate(Sum('score'))['score__sum']
            # scc = 0 if not scc else scc
            score = sc# + scc
            allScore += score
            allCost += cost
            allRound += round
            gameids = GameID.objects.filter(player=player).values("gameid").distinct()
            playerAry.append({
                "id": player.id,
                "name": player.nick_name,
                "gameids": gameids,
                "score": score,
                "cost": cost,
                "round": round,
            })
        introDict["players"] = playerAry
        introDict["allScore"] = allScore
        introDict["allCost"] = allCost
        introDict["allRound"] = allRound
        introDict["count"] = len(playerAry) + 2
        introAry.append(introDict)
    return introAry, total, totalPage

@check_sys_login
def score_change_log(request):
    nickname_search = request.GET.get('nickname','')
    gameid_search = request.GET.get('gameid', '')
    day = datetime.datetime.now().strftime('%Y-%m-%d')
    if request.GET.get('date'):
        day = request.GET.get('date')

    club = Clubs.objects.get(user_name=request.session['club'])
    #列表
    cursor=connection.cursor()
    sql = " select player.id, player.nick_name,"
    sql+= " scorechange.score, scorechange.agent, scorechange.ip, scorechange.create_time"
    sql+= " from DServerAPP_scorechange scorechange join DServerAPP_player player"
    sql+= " on player.id=scorechange.player_id "
    sql+= " where player.club_id='"+str(club.uuid).replace('-','')+"'"
    sql+= " and from_unixtime(scorechange.create_time,'%Y-%m-%d')='"+day+"'"
    sql+= " and is_del=0"
    if nickname_search:
        sql+= " and nick_name like '%"+nickname_search+"%'"
    if gameid_search:
        gameids = GameID.objects.filter(gameid=gameid_search, club=club).values("player_id").distinct()
        if gameids.count() == 0:
            return render(request, 'DServerAPP/score_change_log.html', {'club':club, 'players':[], 'total':0, 'nickname':nickname_search, 'gameid':gameid_search, 'day':day})
        player_id = gameids[0]['player_id']
        sql+= " and player_id="+str(player_id)
    sql+= " order by scorechange.create_time desc"
    cursor.execute(sql)
    players = cursor.fetchall()
    list_ = []
    for player in players:
        gameids = GameID.objects.filter(player_id=player[0])
        timeArray = time.localtime(player[5])
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        data = {
            "id":player[0],
            "nick_name":player[1],
            "score":player[2],
            "agent":player[3],
            "ip":player[4],
            "create_time":create_time,
            "gameids":gameids
        }
        if data['score'] > 0:
            data['change'] = '上分'
        else:
            data['change'] = '下分 '
        list_.append(data)
    total = len(list_)
    #今日统计
    cursor=connection.cursor()
    sql = " select sum(score) score "
    sql+= " from DServerAPP_scorechange scorechange join DServerAPP_player player"
    sql+= " on player.id=scorechange.player_id "
    sql+= " where player.club_id='"+str(club.uuid).replace('-','')+"'"
    sql+= " and from_unixtime(scorechange.create_time,'%Y-%m-%d')='"+day+"'"
    sql+= " and score>0"
    cursor.execute(sql)
    rr = cursor.fetchall()
    today_up = 0
    if rr[0][0]:
        today_up = rr[0][0]
    cursor=connection.cursor()
    sql = " select sum(score) score "
    sql+= " from DServerAPP_scorechange scorechange join DServerAPP_player player"
    sql+= " on player.id=scorechange.player_id "
    sql+= " where player.club_id='"+str(club.uuid).replace('-','')+"'"
    sql+= " and from_unixtime(scorechange.create_time,'%Y-%m-%d')='"+day+"'"
    sql+= " and score<0"
    cursor.execute(sql)
    rr = cursor.fetchall()
    today_down = 0
    if rr[0][0]:
        today_down = rr[0][0]
    return render(request, 'DServerAPP/score_change_log.html', {'club':club, 'players':list_, 'total':total, 'nickname':nickname_search, 'gameid':gameid_search, 'day':day, 'today_up':today_up, 'today_down':today_down})

@check_sys_login
def nick_players(request):
    nickname = request.POST.get('nick', '')
    gameid = request.POST.get('gameid', '')
    club = Clubs.objects.get(user_name=request.session['club'])
    players = Player.objects.filter(club=club, nick_name__contains=nickname, is_del=0)
    if gameid:
        gps = GameID.objects.filter(gameid=gameid, club=club).values("player").distinct()
        players = players.filter(id__in=gps)
    ary = []
    for player in players:

        curPlayer = {}
        curPlayer["id"] = player.id
        curPlayer["wechat_nick_name"] = player.wechat_nick_name
        curPlayer["nick_name"] = player.nick_name
        curPlayer["current_score"] = player.current_score
        ary.append(curPlayer)

    return HttpResponse(json.dumps({"result": 0, "players": ary}), content_type="application/json")

def append_member(request):
    pid = request.POST.get("pid", "")
    cid = request.POST.get("cid", "")
    code = 0
    errmsg = ""

    if pid == "" or cid == "":
        code = 1
        errmsg = "参数不全"
    else:
        if Player.objects.filter(id=pid, introducer=cid).count() > 0:
            code = 3
            errmsg = "该玩家已在本队伍中"
        elif Player.objects.filter(id=pid).exclude(introducer=cid).exclude(introducer=None).count() > 0:
            code = 3
            errmsg = "该玩家已在别的队伍中，请删除后再操作"
        else:
            try:
                player = Player.objects.get(id=pid)
                captain = Captain.objects.get(id=cid)
                player.introducer = captain
                player.save()
            except Player.DoesNotExist:
                code = 2
                errmsg = "玩家查找失败，请稍后重试"
            except Captain.DoesNotExist:
                code = 2
                errmsg = "队长查找失败，请稍后重试"
            except:
                code = 2
                errmsg = "更新失败，请稍后重试"


    result = {"result": code, "errmsg": errmsg}
    return HttpResponse(json.dumps(result), content_type="application/json")

@check_sys_login
def del_member(request):
    pid = request.POST.get("pid", "")
    code = 0
    errmsg = ""

    if pid == "":
        code = 1
        errmsg = "参数不全"
    else:
            try:
                player = Player.objects.get(id=pid)
                player.introducer = None
                player.save()
            except Player.DoesNotExist:
                code = 2
                errmsg = "玩家查找失败，请稍后重试"
            except:
                code = 2
                errmsg = "更新失败，请稍后重试"


    result = {"result": code, "errmsg": errmsg}
    return HttpResponse(json.dumps(result), content_type="application/json")

@check_sys_login
def wrong_image(request):
    club = Clubs.objects.get(user_name=request.session['club'])

    cursor=connection.cursor()
    sql = " select id, image, create_time from DServerAPP_wrongimage"
    sql+= " where club_name='" +club.user_name + "'"
    cursor.execute(sql)
    objs = cursor.fetchall()

    list_ = []
    for obj in objs:
        timeArray = time.localtime(obj[2])
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        club_path = settings.STATIC_URL + 'upload/' + club.user_name + '/'

        data = {
            "id":obj[0],
            "image":club_path + obj[1],
            "create_time":create_time,
        }
        list_.append(data)
    total = len(list_)
    return render(request, 'DServerAPP/wrong_image.html', {'club':club, 'list':list_, 'total': total})

def delete_wrongimage(request):
    second_password = request.POST.get("second_password")
    club = Clubs.objects.get(user_name=request.session['club'])
    result = {'result': 0}
    if second_password != club.password2:
        result["result"] = 1
        result["errmsg"] = "二级密码不正确"
    else:
        wrong_id = request.POST.get('id')
        del_all = request.POST.get('all', 0)
        if del_all == "1":
            WrongImage.objects.filter(club_name=club.user_name).delete()
        elif wrong_id != "":
            WrongImage.objects.filter(id=wrong_id).delete()

    return HttpResponse(json.dumps(result), content_type="application/json")

@check_sys_login
def setting(request):
    club = Clubs.objects.get(user_name=request.session['club'])
    params = club.cost_param.split("|")
    manager = Manager.objects.filter(club=club)
    return render(request, 'DServerAPP/setting.html', {'club':club, 'params':params, 'manager':manager})

def update_cost_mode(request):
    mode = int(request.POST.get('mode'))
    param1 = request.POST.get('param1')
    param2 = request.POST.get('param2')
    param3 = request.POST.get('param3')
    if param1:
        param1 = param1.strip()
    if param2:
        param2 = param2.strip()
    if param3:
        param3 = param3.strip()

    if mode == 0:
        if not is_number(param1) or not is_number(param3):
            return HttpResponse(json.dumps({'result': 1}), content_type="application/json")
        list_ = param2.split('_')
        for index, x in enumerate(list_):
            x = x.strip()
            list_[index] = x
            if not is_number(x):
                return HttpResponse(json.dumps({'result': 1}), content_type="application/json")
        if len(list_) < int(param1):
            return HttpResponse(json.dumps({'result': 1}), content_type="application/json")
        param2 = '_'.join(list_)
    elif mode == 1:
        list1_ = param2.split('*')
        list2_ = param3.split('*')
        logger.info(str(len(list1_)) +'----' + str(len(list2_)))

        if len(list1_) != len(list2_):
            return HttpResponse(json.dumps({'result': 1}), content_type="application/json")

        for index, p in enumerate(list1_):
            range_ = p.split('_')
            cost_ = list2_[index].split('_')
            logger.info(str(len(range_)) +'----' + str(len(cost_)))
            logger.info(list2_[index])
            if len(range_) != len(cost_):
                return HttpResponse(json.dumps({'result': 1}), content_type="application/json")
    elif mode == 2:
        list1_ = param1.split('_')
        for index, x in enumerate(list1_):
            x = x.strip()
            list1_[index] = x
            logger.info('x-'+str(x))
            if not x.isdigit():
                return HttpResponse(json.dumps({'result': 1}), content_type="application/json")
        param1 = '_'.join(list1_)

        list2_ = param2.split('_')
        for index, x in enumerate(list2_):
            x = x.strip()
            list2_[index] = x
            if not x.isdigit():
                return HttpResponse(json.dumps({'result': 1}), content_type="application/json")
        if len(list1_) != len(list2_):
            return HttpResponse(json.dumps({'result': 1}), content_type="application/json")
        param2 = '_'.join(list2_)

    club = Clubs.objects.get(user_name=request.session['club'])
    club.cost_mode = mode
    if mode == 0:
        club.cost_param = '%s|%s|%s' % (param1, param2, param3)
    elif mode == 1:
        club.cost_param = '%s|%s|%s' % (param1, param2, param3)
    else:
        club.cost_param = '%s|%s' % (param1, param2)

    club.save()
    return HttpResponse(json.dumps({'result': 0}), content_type="application/json")

def update_refresh_time(request):
    refresh_time = int(request.POST.get('refresh_time'))
    club = Clubs.objects.get(user_name=request.session['club'])
    club.refresh_time = refresh_time
    club.save()
    return HttpResponse(json.dumps({'result': 0}), content_type="application/json")

def del_data(request):
    second_password = request.POST.get("second_password")
    club = Clubs.objects.get(user_name=request.session['club'])
    result = {'result': 0}
    if second_password != club.password2:
        result["result"] = 1
        result["errmsg"] = "二级密码不正确"
    else:
        cursor=connection.cursor()
        sql = " delete from DServerAPP_historygame"
        sql+= " where club_id='" +str(club.uuid).replace('-','') + "'"
        cursor.execute(sql)
        sql = " update DServerAPP_player"
        sql+= " set current_score=0,history_profit=0,today_hoster_number=0,history_cost=0"
        sql+= " where club_id='" +str(club.uuid).replace('-','') + "'"
        cursor.execute(sql)
        sql = " delete from DServerAPP_score"
        sql+= " where player_id in ("
        sql+= " select id from DServerAPP_player where club_id='" +str(club.uuid).replace('-','') + "'"
        sql+= ")"
        cursor.execute(sql)
    return HttpResponse(json.dumps(result), content_type="application/json")

def stat_xls(request):
    cid = request.GET.get('cid', None)
    if not cid:
        return HttpResponse("参数无效，请返回重试")

    club = Clubs.objects.get(user_name=cid)
    players = Player.objects.filter(club=club, is_del=0).order_by('-current_score')
    wb = xlwt.Workbook()
    wb.encoding = 'utf-8'
    ws = wb.add_sheet('总账单')

    total_plus = 0
    total_minus = 0
    plus_row1 = 1
    plus_row2 = 2
    minus_row1 = 5
    minus_row2 = 6
    title_style1 = stat_xls_style(3, 'SimSun', 400, 0, True)
    title_style2 = stat_xls_style(7, 'SimSun', 400, 0, True)
    text_style = stat_xls_style(1, 'SimSun', 300, 0, False)
    num_style = stat_xls_style(1, 'Arial', 300, 0, False)

    ws.col(plus_row1).width = 256 * 30
    ws.col(plus_row2).width = 256 * 20

    ws.col(minus_row1).width = 256 * 30
    ws.col(minus_row2).width = 256 * 20



    ws.write(0, 1, '名字', title_style1)  #如果要写中文请使用UNICODE
    ws.write(0, 2, '正数', title_style2)  #如果要写中文请使用UNICODE
    index = 0
    for player in players:
        if player.current_score < 0:
            continue
        ws.write(index + 1, plus_row1, player.nick_name, text_style)  #如果要写中文请使用UNICODE
        ws.write(index + 1, plus_row2, player.current_score, num_style)  #如果要写中文请使用UNICODE
        total_plus += player.current_score
        index += 1
    ws.write(index + 1, plus_row1, '总数', title_style1)  #如果要写中文请使用UNICODE
    ws.write(index + 1, plus_row2, total_plus, title_style2)  #如果要写中文请使用UNICODE


    ws.write(0, 5, '名字', title_style1)  #如果要写中文请使用UNICODE
    ws.write(0, 6, '负数', title_style2)  #如果要写中文请使用UNICODE
    index = 0
    for player in players:
        if player.current_score >= 0:
            continue
        ws.write(index + 1, minus_row1, player.nick_name, text_style)  #如果要写中文请使用UNICODE
        ws.write(index + 1, minus_row2, player.current_score, num_style)  #如果要写中文请使用UNICODE
        total_minus += player.current_score
        index += 1
    ws.write(index + 1, minus_row1, '总数', title_style1)  #如果要写中文请使用UNICODE
    ws.write(index + 1, minus_row2, total_minus, title_style2)  #如果要写中文请使用UNICODE

    sio = io.BytesIO()
    wb.save(sio)   #这点很重要，传给save函数的不是保存文件名，而是一个StringIO流
    sio.seek(0)
    res = HttpResponse()
    res["Content-Type"] = "application/vnd.ms-excel"
    res["Content-Disposition"] = 'filename="总账单.xls"'
    res.write(sio.getvalue())
    return res

def stat_xls_style(bg_color, name, height, color, bold=False):
    style = xlwt.XFStyle()  # 初始化样式

    pattern = xlwt.Pattern()   # 创建一个模式
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN # 设置其模式为实型
    pattern.pattern_fore_colour = bg_color

    font = xlwt.Font()  # 为样式创建字体
    # 字体类型：比如宋体、仿宋也可以是汉仪瘦金书繁
    font.name = name
    # 设置字体颜色
    font.colour_index = color
    # 字体大小
    font.height = height

    borders = xlwt.Borders()
    borders.left = xlwt.Borders.THIN
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN

    # 定义格式
    style.font = font
    style.borders = borders
    style.pattern = pattern

    return style


