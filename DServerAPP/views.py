# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Clubs, Cdkey
import uuid
from django.utils import timezone
from . import messageType
import itchat
import _thread
from . import wechatManager
import time,datetime,json

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
    print(username)

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
        club = Clubs(uuid=uuid.uuid1(), user_name = username, password=password, expired_time=time.time())
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

def bind_wechat(request):
    club = request.GET.get('club','')

    bot = wechatManager.wechatInstance.new_instance(club)
    logined, qrid = bot.check_login()
    print(qrid)
    return HttpResponseRedirect('https://wx.qq.com/qrcode/'+qrid)
    #return render(request, 'DServerAPP/index.html', {"pwd": 1, "pwct": "两次密码不一致"})

    #return HttpResponse(messageType.createMessage('success', messageType.CLUB_NOT_EXIST, qrid))

    '''
     thread = wechatManager.wechatInstance(club)
     thread.start()
     try:
        clubInstance = Clubs.objects.get(user_name=club)
        if clubInstance.expired_time > time.time():
             return HttpResponse('club='+club)
        else:
             return HttpResponse(messageType.createMessage('success', messageType.CLUB_EXPIRED, '用户需要付费'))
     except Clubs.DoesNotExist:
        return HttpResponse(messageType.createMessage('success', messageType.CLUB_NOT_EXIST, 'the club not exist'))
    '''
