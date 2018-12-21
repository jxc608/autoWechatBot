# -*- coding: utf-8 -*-
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('registerPage', views.registerPage, name='registerPage'),
    path('register', views.register, name='register'),
    path('login_password', views.login_password, name='login_password'),
    # path('login_smscode', views.login_smscode, name='login_smscode'),
    # wx
    path('check_wx_login', views.check_wx_login, name='check_wx_login'),
    path('add_time', views.add_time, name='add_time'),
    path('create_cdkey', views.create_cdkey, name='create_cdkey'),
    path('get_cdkey', views.get_cdkey, name='get_cdkey'),
    # wx
    path('get_uuid', views.get_uuid, name='get_uuid'),
    # wx
    path('wx_logout', views.wx_logout, name='wx_logout'),
    path('room_data', views.room_data, name='room_data'),
    path('clear_room_data', views.clear_room_data, name='clear_room_data'),
    path('player_data', views.player_data, name='player_data'),
    path('add_player', views.add_player, name='add_player'),
    # wx
    path('wechat_bind', views.wechat_bind, name='wechat_bind'),
    path('wrong_image', views.wrong_image, name='wrong_image'),
    path('setting', views.setting, name='setting'),
    path('update_cost_mode', views.update_cost_mode, name='update_cost_mode'),
    path('del_data', views.del_data, name='del_data'),
    path('player_stat', views.player_stat, name='player_stat'),
    path('clear_player_stat', views.clear_player_stat, name='clear_player_stat'),
    path('player_room_data', views.player_room_data, name='player_room_data'),
    path('delete_wrongimage', views.delete_wrongimage, name='delete_wrongimage'),
    # wx
    path('add_score', views.add_score, name='add_score'),
    # wx
    path('minus_score', views.minus_score, name='minus_score'),
    path('score_change', views.score_change, name='score_change'),
    path('score_change_log', views.score_change_log, name='score_change_log'),
    path('add_gameid', views.add_gameid, name='add_gameid'),
    path('del_gameid', views.del_gameid, name='del_gameid'),
    # wx
    path('wechat_friends', views.wechat_friends, name='wechat_friends'),
    path('stat_xls', views.stat_xls, name='stat_xls'),
    # path('bot_get_uuid', views.bot_get_uuid, name='bot_get_uuid'),
    # path('bot_check_login', views.bot_check_login, name='bot_check_login'),
    # path('bot_logout', views.bot_logout, name='bot_logout'),
    # path('bot_wechat_friends', views.bot_wechat_friends, name='bot_wechat_friends'),
    # path('bot_wechat_bind', views.bot_wechat_bind, name='bot_wechat_bind'),
    path('del_player', views.del_player, name='del_player'),
    path('change_passwd', views.change_passwd, name='change_passwd'),
    #path('wechat_bind_all', views.wechat_bind_all, name='wechat_bind_all'),
    #path('bot_wechat_bind_all', views.bot_wechat_bind_all, name='bot_wechat_bind_all'),
    # path('bot_notice', views.bot_notice, name='bot_notice'),
    path('add_score_limit', views.add_score_limit, name='add_score_limit'),
    # wx
    path('add_manager', views.add_manager, name='add_manager'),
    # path('bot_wechat_bind_manager', views.bot_wechat_bind_manager, name='bot_wechat_bind_manager'),
    path('del_manager', views.del_manager, name='del_manager'),
    path('update_refresh_time', views.update_refresh_time, name='update_refresh_time'),

]