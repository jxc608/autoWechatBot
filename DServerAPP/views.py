# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Clubs
import uuid
from django.utils import timezone
from . import messageType
import itchat
import _thread
from . import wechatManager
import time

def index(request):
    return render(request, 'DServerAPP/index.html')

def registerPage(request):
    return render(request, 'DServerAPP/register.html')

def register(request):
    username=request.POST.get('username','')
    password=request.POST.get('password','')
    cpassword=request.POST.get('cpassword','')
    print(username)

    if username == None:
        return render(request, 'DServerAPP/index.html', {"account": 1, "acct":"账号为空" })
    elif password == '': 
        return render(request, 'DServerAPP/index.html', {"pwd": 1, "pwct": "密码为空"})
    elif  password != cpassword:
        return render(request, 'DServerAPP/index.html', {"pwd": 1, "pwct": "两次密码不一致"})
    

    try:
        club = Clubs.objects.get(user_name=username)
        return HttpResponse(messageType.createMessage('success', messageType.USER_NAME_ALREADY_USED, 'the userName has already been used'))
    except Clubs.DoesNotExist:
        password=request.POST.get('password','')
        club = Clubs(uuid=uuid.uuid1(), user_name = username, password=password, expired_time=time.time())
        club.save()
        return HttpResponse(messageType.createMessage('success', messageType.SUCCESS, 'register completed'))

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
                return render(request, 'DServerAPP/index.html', {"pwd": 1, "pwct": "密码错误"})
            else:
                #登录成功之后，渲染页面
                return render(request, 'DServerAPP/login_succ.html', {"codeSrc": "https://gss0.bdstatic.com/94o3dSag_xI4khGkpoWK1HF6hhy/baike/s%3D220/sign=660c358c4aed2e73f8e9812eb700a16d/08f790529822720e5c8538f27bcb0a46f21fab6b.jpg"})
        except Clubs.DoesNotExist:
            return render(request, 'DServerAPP/index.html', {"pwd": 1, "pwct": "账号不存在"})
    
   

def login_smscode(request):
    username=request.POST.get('username','')
    smscode=request.POST.get('smscode','')
    return HttpResponse('username='+username+"&password="+password)

def add_time(request):
    username=request.POST.get('username','')
    cdkey=request.POST.get('cdkey','')
    try:
        clubInstance = Clubs.objects.get(user_name=username)
        clubInstance.expired_time = time.time() + 2592000
        clubInstance.save()
        return HttpResponse(messageType.createMessage('success', messageType.SUCCESS, 'add time succeed'))
    except Clubs.DoesNotExist:
        return HttpResponse(messageType.createMessage('success', messageType.CLUB_NOT_EXIST, 'the club not exist'))

def bind_wechat(request):
    club = request.GET.get('club','')

    bot = wechatManager.wechatInstance.new_instance(club)
    logined, qrid = bot.check_login()
    print('logined:'+str(logined))
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
