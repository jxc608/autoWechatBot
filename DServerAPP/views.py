# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
import re
import uuid
from django.utils import timezone
from . import messageType
import itchat
import _thread
from . import wechatManager
import time,datetime,json
from django.db import connection
from django.conf import settings
from django.db.models import Sum
import xlwt
import io

def timestamp2string(timeStamp): 
  try: 
    d = datetime.datetime.fromtimestamp(timeStamp) 
    str1 = d.strftime("%Y-%m-%d %H:%M:%S") 
    # 2015-08-28 16:43:37.283000' 
    return str1 
  except Exception as e: 
    print(e)
    return '' 

def is_login(request):
    if not request.session.get('login') or  request.session.get('login') == False:
        return False
    else:
        return True

def index(request):
    if is_login(request) == False:
        return HttpResponseRedirect('/login')
    club = Clubs.objects.get(user_name=request.session['club'])
    club.expired = False
    if club.expired_time < time.time():
        club.expired_time_desc = '已失效'
        club.expired = True
    else:
        club.expired_time_desc = timestamp2string(club.expired_time)

    bot = wechatManager.wechatInstance.new_instance(club.user_name)
    wx_login = bot.is_login()
    uuid = None
    if not wx_login and not club.expired:
        uuid = bot.get_uuid()
        bot.check_login(uuid)
    is_admin = False
    if club.user_name == '18811333964':
        is_admin = True
    return render(request, 'DServerAPP/index.html', {'club':club, 'wx_login':wx_login, 'uuid':uuid, 'is_admin':is_admin})

def get_uuid(request):
    bot = wechatManager.wechatInstance.new_instance(request.session['club'])
    bot.checked = False
    uuid = bot.get_uuid()
    bot.check_login(uuid)
    return HttpResponse(json.dumps({'uuid': uuid}), content_type="application/json")

def login(request):
    return render(request, 'DServerAPP/login.html')

def logout(request):
    del request.session['login']
    del request.session['club']
    return HttpResponseRedirect('/login')

def registerPage(request):
    return render(request, 'DServerAPP/register.html')

def register(request):
    username=request.POST.get('username','')
    password=request.POST.get('password','')
    cpassword=request.POST.get('cpassword','')

    if username == None:
        return render(request, 'DServerAPP/register.html', {"account": 1, "acct":"账号为空" })
    elif password == '': 
        return render(request, 'DServerAPP/register.html', {"pwd": 1, "pwct": "密码为空"})
    elif  password != cpassword:
        return render(request, 'DServerAPP/register.html', {"pwd": 1, "pwct": "两次密码不一致"})

    try:
        club = Clubs.objects.get(user_name=username)
        return render(request, 'DServerAPP/register.html', {"account": 1, "acct":"账号已注册" })
        #return HttpResponse(messageType.createMessage('success', messageType.USER_NAME_ALREADY_USED, 'the userName has already been used'))
    except Clubs.DoesNotExist:
        password=request.POST.get('password','')
        club = Clubs(uuid=uuid.uuid1(), user_name = username, password=password, expired_time=time.time(), cost_mode=0, cost_param='')
        club.save()
        return render(request, 'DServerAPP/register.html', {"account": 2, "acct":"注册成功！" })
        #return HttpResponse(messageType.createMessage('success', messageType.SUCCESS, 'register completed'))

def login_password(request):
    username=request.POST.get('username','')
    password=request.POST.get('password','')
    if username == '':
        return render(request, 'DServerAPP/index.html', {"account": 1, "acct":"账号为空" })
    elif password == '':
        return render(request, 'DServerAPP/index.html', {"pwd": 1, "pwct": "密码为空"})
    else:
        try:
            club = Clubs.objects.get(user_name=username)
            if club.password != password:
                return render(request, 'DServerAPP/login.html', {"pwd": 1, "pwct": "密码错误"})
            else:
                request.session['login'] = True;
                request.session['club'] = username;
                #登录成功之后，渲染页面
                return HttpResponseRedirect('/')
                #return render(request, 'DServerAPP/login_succ.html', {"codeSrc": "https://gss0.bdstatic.com/94o3dSag_xI4khGkpoWK1HF6hhy/baike/s%3D220/sign=660c358c4aed2e73f8e9812eb700a16d/08f790529822720e5c8538f27bcb0a46f21fab6b.jpg"})
        except Clubs.DoesNotExist:
            return render(request, 'DServerAPP/login.html', {"pwd": 1, "pwct": "账号不存在"})
    
   
def login_smscode(request):
    username=request.POST.get('username','')
    smscode=request.POST.get('smscode','')
    return HttpResponse('username='+username+"&password="+password)

def add_time(request):
    username=request.session['club'];
    cdkey=request.POST.get('cdkey')
    try:
        keyInstance = Cdkey.objects.get(cdkey=cdkey)
        if keyInstance.status == 1:
            return HttpResponse(messageType.createMessage('success', messageType.CDKEY_USED, 'the cdkey used'))
        time_add = 0
        if keyInstance.key_type == 1:
            time_add = 3600
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
        keyInstance.save()
        return HttpResponse(messageType.createMessage('success', messageType.SUCCESS, 'add time succeed'))
    except Clubs.DoesNotExist:
        return HttpResponse(messageType.createMessage('success', messageType.CLUB_NOT_EXIST, 'the club not exist'))


def check_wx_login(request):
    bot = wechatManager.wechatInstance.new_instance(request.session['club'])
    wx_login = bot.is_login()

    return HttpResponse(json.dumps({'login': wx_login}), content_type="application/json")

def wx_logout(request):
    bot = wechatManager.wechatInstance.new_instance(request.session['club'])
    bot.logout()
    return HttpResponse(json.dumps({'result': True}), content_type="application/json")

def create_cdkey(request):
    if request.session['club'] != '18811333964':
        return

    key_type = int(request.POST.get('key_type'))
    num = int(request.POST.get('num'))
    for x in range(0, num):
        key = Cdkey()
        key.cdkey = str(uuid.uuid1())[:8]
        key.key_type = key_type
        key.status = 0
        key.create_time = int(time.time())
        key.save()
    return HttpResponse(json.dumps({'result': True}), content_type="application/json")

def get_cdkey(request):
    key_type = int(request.POST.get('key_type'))
    num = int(request.POST.get('num'))
    keys = Cdkey.objects.filter(status=0, key_type=key_type)[:num]
    result = []
    for key in keys:
        result.append(key.cdkey)
    return HttpResponse(json.dumps({'result': result}), content_type="application/json")

def room_data(request):
    day = datetime.datetime.now().strftime('%Y-%m-%d')
    if request.GET.get('date'):
        day = request.GET.get('date')
    orderby = request.GET.get('order', 'round')

    club = Clubs.objects.get(user_name=request.session['club'])
    rooms = HistoryGame.objects.filter(club=club, create_time__startswith=day)
    total_cost = 0
    total_score = 0
    total_round = 0
    total_profit = 0
    for room in rooms:
        total_cost += room.cost
        total_score += room.score
        total_round += room.round_number
        total_profit += room.score - room.cost

    if orderby == 'cost':  
        rooms = sorted(rooms, key=lambda rooms : rooms.cost, reverse=True) 
    elif orderby == 'score':  
        rooms = sorted(rooms, key=lambda rooms : rooms.score, reverse=True) 
    elif orderby == 'round':  
        rooms = sorted(rooms, key=lambda rooms : rooms.round_number, reverse=True)
    total = len(rooms)

    return render(request, 'DServerAPP/room_data.html', {'rooms':rooms, 'total':total, 'total_cost':total_cost, 'total_score':total_score, 'total_round':total_round, 'total_profit':total_profit, 'day':day})

def player_room_data(request):
    club = Clubs.objects.get(user_name=request.session['club'])
    day = datetime.datetime.now().strftime('%Y-%m-%d')
    if request.GET.get('date'):
        day = request.GET.get('date')
    orderby = request.GET.get('order', 'round')
    players = Player.objects.filter(club=club).order_by('-current_score', '-history_profit')

    for player in players:
        player.gameids = GameID.objects.filter(player_id=player.id)
        player.total_round = Score.objects.filter(player_id=player.id, create_time__startswith=day).count()
        player.total_cost = Score.objects.filter(player_id=player.id, create_time__startswith=day).aggregate(Sum('cost'))['cost__sum']
        if player.total_cost == None:
            player.total_cost = 0
        player.total_score = Score.objects.filter(player_id=player.id, create_time__startswith=day).aggregate(Sum('score'))['score__sum']
        if player.total_score == None:
            player.total_score = 0    
        player.total_host = Score.objects.filter(player_id=player.id, create_time__startswith=day).aggregate(Sum('is_host'))['is_host__sum']
        if player.total_host == None:
            player.total_host = 0
    if orderby == 'round':  
        players = sorted(players, key=lambda players : players.total_round, reverse=True) 
    elif orderby == 'host':  
        players = sorted(players, key=lambda players : players.total_host, reverse=True)
    elif orderby == 'score':  
        players = sorted(players, key=lambda players : players.total_score, reverse=True)
    elif orderby == 'cost':  
        players = sorted(players, key=lambda players : players.total_cost, reverse=True)
    return render(request, 'DServerAPP/player_room_data.html', {'players':players,'day':day})
    
def player_data(request):
    nickname_search = request.GET.get('nickname','')
    gameid_search = request.GET.get('gameid', '')
    club = Clubs.objects.get(user_name=request.session['club'])
    player_id = 0
    if gameid_search:
        gameids = GameID.objects.filter(gameid=gameid_search, club=club).values("player_id").distinct()
        if gameids.count() == 0:
            return render(request, 'DServerAPP/player_data.html', {'club':club, 'players':[], 'total':0, 'nickname':nickname_search, 'gameid':gameid_search})
        player_id = gameids[0]['player_id']
    if gameid_search:        
        players = Player.objects.filter(club=club, id=player_id).order_by('-current_score')
    elif nickname_search:
        players = Player.objects.filter(club=club, nick_name__contains=nickname_search).order_by('-current_score')
    else:
        players = Player.objects.filter(club=club).order_by('-current_score', '-history_profit')

    for player in players:
        gameids = GameID.objects.filter(player_id=player.id)
        player.gameids = gameids

    total = len(players)
    return render(request, 'DServerAPP/player_data.html', {'club':club, 'players':players, 'total':total, 'nickname':nickname_search, 'gameid':gameid_search})


def player_stat(request):
    nickname_search = request.GET.get('nickname','')
    gameid_search = request.GET.get('gameid', '')
    club = Clubs.objects.get(user_name=request.session['club'])

    if nickname_search:
        players_cost = Player.objects.filter(club=club, nick_name__contains=nickname_search).order_by('-history_cost')
    else:
        players_cost = Player.objects.filter(club=club).order_by('-history_cost')

    for player in players_cost:
        gameids = GameID.objects.filter(player_id=player.id)
        player.gameids = gameids

    if nickname_search:
        players_profit = Player.objects.filter(club=club, nick_name__contains=nickname_search).order_by('-history_profit')
    else:
        players_profit = Player.objects.filter(club=club).order_by('-history_profit')

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

def add_player(request):
    nickname = request.POST.get('nickname')
    gameid = int(request.POST.get('gameid'))

    club = Clubs.objects.get(user_name=request.session['club'])

    player = None
    try:
        player = Player.objects.get(nick_name=nickname, club=club)
        return HttpResponse(json.dumps({'result': 1}), content_type="application/json")
    except Player.DoesNotExist:
        pass

    gameID = GameID.objects.filter(gameid=gameid, club=club)
    if len(gameID) > 0:
        return HttpResponse(json.dumps({'result': 2}), content_type="application/json")

    player = Player(wechat_nick_name='tempUser', nick_name=nickname, club=club, current_score=0, history_profit=0)
    player.save()
    gameid = GameID(player=player, club=club, gameid=gameid, game_nick_name=nickname)
    gameid.save()

    return HttpResponse(json.dumps({'result': 0}), content_type="application/json")

def add_gameid(request):
    player_id = int(request.POST.get('id'))
    gameid = int(request.POST.get('gameid'))

    club = Clubs.objects.get(user_name=request.session['club'])

    player = None
    try:
        player = Player.objects.get(id=player_id, club=club)
    except Player.DoesNotExist:
        return HttpResponse(json.dumps({'result': 1}), content_type="application/json")

    gameID = GameID.objects.filter(gameid=gameid, club=club)
    if len(gameID) > 0:
        player_id = gameID[0].player_id
        ids_count = GameID.objects.filter(player_id=player_id).values("gameid").distinct().count()
        if ids_count > 1:
            return HttpResponse(json.dumps({'result': 2}), content_type="application/json")
        GameID.objects.filter(player_id=player_id).update(player_id=player.id)
        Score.objects.filter(player_id=player_id).update(player_id=player.id)
        ScoreChange.objects.filter(player_id=player_id).update(player_id=player.id)
        original_player = Player.objects.get(id=player_id)
        player.current_score += original_player.current_score
        player.history_profit += original_player.history_profit
        player.history_cost += original_player.history_cost
        player.today_hoster_number += original_player.today_hoster_number
        player.save()
        original_player.delete()
    else:
        gameid = GameID(player=player, club=club, gameid=gameid, game_nick_name=player.nick_name)
        gameid.save()

    return HttpResponse(json.dumps({'result': 0}), content_type="application/json")

def del_gameid(request):
    player_id = int(request.POST.get('id'))
    gameid = int(request.POST.get('gameid'))

    club = Clubs.objects.get(user_name=request.session['club'])

    player = None
    try:
        player = Player.objects.get(id=player_id, club=club)
    except Player.DoesNotExist:
        return HttpResponse(json.dumps({'result': 1}), content_type="application/json")
    GameID.objects.filter(player_id=player_id, gameid=gameid).delete()

    return HttpResponse(json.dumps({'result': 0}), content_type="application/json")


def wechat_friends(request):
    player_id = int(request.POST.get('id'))
    nick_name = request.POST.get('nick_name')
    wechat_nick_name = request.POST.get('wechat_nick_name')

    club = Clubs.objects.get(user_name=request.session['club'])

    bot = wechatManager.wechatInstance.new_instance(club.user_name)
    wx_login = bot.is_login()
    uuid = None
    if not wx_login or club.expired_time < time.time():
        return HttpResponse(json.dumps({'result': 2}), content_type="application/json")

    list_ = bot.search_friends(wechat_nick_name)

    return HttpResponse(json.dumps({'result': 0, 'list':list_}), content_type="application/json")


def wechat_bind(request):
    player_id = int(request.POST.get('id'))
    user_name = request.POST.get('user_name')
    nick_name = request.POST.get('nick_name')
    wechat_nick_name = request.POST.get('wechat_nick_name')

    club = Clubs.objects.get(user_name=request.session['club'])

    bot = wechatManager.wechatInstance.new_instance(club.user_name)
    wx_login = bot.is_login()
    uuid = None
    if not wx_login or club.expired_time < time.time():
        return HttpResponse(json.dumps({'result': 2}), content_type="application/json")

    code, msg = bot.set_alias(user_name, nick_name)
    if code == 0:
        player = Player.objects.get(id=player_id)
        if player.club_id != club.uuid:
            return HttpResponse(json.dumps({'result': 1}), content_type="application/json")
        player.nick_name = nick_name
        player.wechat_nick_name = wechat_nick_name
        #player.current_score = score
        #player.history_profit = profit
        player.save()
        return HttpResponse(json.dumps({'result': 0}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'result': 3, 'msg':msg}), content_type="application/json")


def add_score(request):
    player_id = int(request.POST.get('id'))
    score = int(request.POST.get('score'))

    club = Clubs.objects.get(user_name=request.session['club'])
    player = Player.objects.get(id=player_id)
    if player.club_id != club.uuid:
        return HttpResponse(json.dumps({'result': 1}), content_type="application/json")
    player.current_score += score
    player.save()
    agent = request.ua.os
    '''
    'device_type': request.ua.device_type,
    'os': request.ua.os,
    'browser': request.ua.browser,
    'from_pc': request.ua.from_pc,
    'from_smartphone': request.ua.from_pc,
    '''
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']

    score_change = ScoreChange(player=player, score=score, agent=agent, ip=ip, create_time=int(time.time()))
    score_change.save();
    return HttpResponse(json.dumps({'result': 0, 'current_score':player.current_score}), content_type="application/json")

def minus_score(request):
    player_id = int(request.POST.get('id'))
    score = int(request.POST.get('score'))

    club = Clubs.objects.get(user_name=request.session['club'])
    player = Player.objects.get(id=player_id)
    if player.club_id != club.uuid:
        return HttpResponse(json.dumps({'result': 1}), content_type="application/json")
    player.current_score -= score
    player.save()
    agent = request.ua.os
    '''
    'device_type': request.ua.device_type,
    'os': request.ua.os,
    'browser': request.ua.browser,
    'from_pc': request.ua.from_pc,
    'from_smartphone': request.ua.from_pc,
    '''
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']

    score_change = ScoreChange(player=player, score=-score, agent=agent, ip=ip, create_time=int(time.time()))
    score_change.save();

    return HttpResponse(json.dumps({'result': 0, 'current_score':player.current_score}), content_type="application/json")

def score_change(request):
    nickname_search = request.GET.get('nickname','')
    gameid_search = request.GET.get('gameid', '')
    orderby = request.GET.get('order', 'round')
    club = Clubs.objects.get(user_name=request.session['club'])

    player_id = 0
    if gameid_search:
        gameids = GameID.objects.filter(gameid=gameid_search, club=club).values("player_id").distinct()
        if gameids.count() == 0:
            return render(request, 'DServerAPP/player_data.html', {'club':club, 'players':[], 'total':0, 'nickname':nickname_search, 'gameid':gameid_search})
        player_id = gameids[0]['player_id']
    if gameid_search:        
        players = Player.objects.filter(club=club, id=player_id).order_by('-current_score')
    elif nickname_search:
        players = Player.objects.filter(club=club, nick_name__contains=nickname_search).order_by('-current_score')
    else:
        players = Player.objects.filter(club=club).order_by('-current_score', '-history_profit')

    for player in players:
        player.gameids = GameID.objects.filter(player_id=player.id)
        player.gameids_count = len(player.gameids)
        player.total_round = Score.objects.filter(player_id=player.id).count()
    if orderby == 'round':
        players = sorted(players, key=lambda players : players.total_round, reverse=True) 
    else:
        players = sorted(players, key=lambda players : players.current_score, reverse=True) 

    total = len(players)
    return render(request, 'DServerAPP/score_change.html', {'club':club, 'players':players, 'total':total, 'nickname':nickname_search, 'gameid':gameid_search})


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
    return render(request, 'DServerAPP/wrong_image.html', {'club':club, 'list':list_})

def delete_wrongimage(request):
    wrong_id = request.POST.get('id')
    del_all = request.POST.get('all', 0)
    club = Clubs.objects.get(user_name=request.session['club'])

    cursor=connection.cursor()
    sql = " delete from DServerAPP_wrongimage"
    sql+= " where club_name='" +club.user_name + "'"
    if wrong_id:
        sql+= " and id=" + wrong_id
    cursor.execute(sql)

    return HttpResponse(json.dumps({'result': 0}), content_type="application/json")

def setting(request):
    club = Clubs.objects.get(user_name=request.session['club'])
    params = club.cost_param.split("|")
    return render(request, 'DServerAPP/setting.html', {'club':club, 'params':params})

def is_number(num):

    regex = re.compile(r"^(-?\d+)(\.\d*)?$")

    if re.match(regex,num):
        return True
    else:
        return False

def update_cost_mode(request):
    mode = int(request.POST.get('mode'))
    param1 = request.POST.get('param1')
    param2 = request.POST.get('param2')
    param3 = request.POST.get('param3')

    if mode == 0:
        if not param1.isdigit() or not param3.isdigit():
            return HttpResponse(json.dumps({'result': 1}), content_type="application/json")
        list_ = param2.split('_')
        for x in list_:
            if not is_number(x):
                return HttpResponse(json.dumps({'result': 1}), content_type="application/json")
        if len(list_) < int(param1):
            return HttpResponse(json.dumps({'result': 1}), content_type="application/json")

    elif mode == 1:
        if not param1.isdigit():
            return HttpResponse(json.dumps({'result': 1}), content_type="application/json")
        list_ = param2.split('_')
        for x in list_:
            if not is_number(x):
                return HttpResponse(json.dumps({'result': 1}), content_type="application/json")
            if float(x) > 1:
                return HttpResponse(json.dumps({'result': 1}), content_type="application/json")
        if len(list_) < int(param1):
            return HttpResponse(json.dumps({'result': 1}), content_type="application/json")

    elif mode == 2:
        list1_ = param1.split('_')
        for x in list1_:
            if not x.isdigit():
                return HttpResponse(json.dumps({'result': 1}), content_type="application/json")
        list2_ = param2.split('_')
        for x in list2_:
            if not x.isdigit():
                return HttpResponse(json.dumps({'result': 1}), content_type="application/json")
        if len(list1_) != len(list2_):
            return HttpResponse(json.dumps({'result': 1}), content_type="application/json")

    club = Clubs.objects.get(user_name=request.session['club'])
    club.cost_mode = mode
    if mode == 0:
        club.cost_param = '%s|%s|%s' % (param1, param2, param3)
    else:
        club.cost_param = '%s|%s' % (param1, param2)

    club.save()
    return HttpResponse(json.dumps({'result': 0}), content_type="application/json")

def del_data(request):
    club = Clubs.objects.get(user_name=request.session['club'])
    cursor=connection.cursor()
    sql = " delete from DServerAPP_historygame"
    sql+= " where club_id='" +str(club.uuid).replace('-','') + "'"
    cursor.execute(sql)
    sql = " update DServerAPP_player"
    sql+= " set current_score=0,history_profit=0,today_hoster_number=0"
    sql+= " where club_id='" +str(club.uuid).replace('-','') + "'"
    cursor.execute(sql)
    sql = " delete from DServerAPP_score"
    sql+= " where player_id in ("
    sql+= " select id from DServerAPP_player where club_id='" +str(club.uuid).replace('-','') + "'"
    sql+= ")"
    cursor.execute(sql)
    return HttpResponse(json.dumps({'result': 0}), content_type="application/json")

def stat_xls(request):
    club = Clubs.objects.get(user_name=request.session['club'])
    players = Player.objects.filter(club=club).order_by('-current_score')
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

    ws.write(0, 1, '名字', title_style1)  #如果要写中文请使用UNICODE
    ws.write(0, 2, '正数', title_style2)  #如果要写中文请使用UNICODE
    index = 0
    for player in players:
        if player.current_score < 0:
            continue
        ws.write(index + 1, plus_row1, player.nick_name, text_style)  #如果要写中文请使用UNICODE
        ws.write(index + 1, plus_row2, player.current_score, num_style)  #如果要写中文请使用UNICODE
        total_plus += player.current_score
        index += 1;
    ws.write(index + 1, plus_row1, '总数', title_style1)  #如果要写中文请使用UNICODE
    ws.write(index + 1, plus_row2, total_plus, title_style2)  #如果要写中文请使用UNICODE


    ws.write(0, 5, '名字', title_style1)  #如果要写中文请使用UNICODE
    ws.write(0, 6, '负数', title_style2)  #如果要写中文请使用UNICODE
    index = 0
    for player in players:
        if player.current_score > 0:
            continue
        ws.write(index + 1, minus_row1, player.nick_name, text_style)  #如果要写中文请使用UNICODE
        ws.write(index + 1, minus_row2, player.current_score, num_style)  #如果要写中文请使用UNICODE
        total_minus += player.current_score
        index += 1;
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


