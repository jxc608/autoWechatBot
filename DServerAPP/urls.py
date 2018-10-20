from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('registerPage', views.registerPage, name='registerPage'),
    path('register', views.register, name='register'),
    path('login_password', views.login_password, name='login_password'),
    path('login_smscode', views.login_smscode, name='login_smscode'),
    path('check_wx_login', views.check_wx_login, name='check_wx_login'),
    path('add_time', views.add_time, name='add_time'),
    path('create_cdkey', views.create_cdkey, name='create_cdkey'),
    path('get_cdkey', views.get_cdkey, name='get_cdkey'),
    path('get_uuid', views.get_uuid, name='get_uuid'),
    path('wx_logout', views.wx_logout, name='wx_logout'),
    path('room_data', views.room_data, name='room_data'),
    path('player_data', views.player_data, name='player_data'),
    path('add_player', views.add_player, name='add_player'),
    path('update_player', views.update_player, name='update_player'),
    path('wrong_image', views.wrong_image, name='wrong_image'),
    path('setting', views.setting, name='setting'),
    path('update_cost_mode', views.update_cost_mode, name='update_cost_mode'),
    path('del_data', views.del_data, name='del_data'),
    path('player_stat', views.player_stat, name='player_stat'),
    path('player_room_data', views.player_room_data, name='player_room_data'),

]