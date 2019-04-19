"""wechat_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.urls import path, include

urlpatterns = [
    path('bot_logout_all', views.logout_all, name='bot_logout_all'),
    path('bot_check_login', views.bot_check_login, name='bot_check_login'),
    path('bot_refresh_uuid', views.bot_refresh_uuid, name='bot_refresh_uuid'),
    path('bot_notice', views.bot_notice, name='bot_notice'),
    path('bot_logout', views.bot_logout, name='bot_logout'),
    path('bot_wechat_bind', views.bot_wechat_bind, name='bot_wechat_bind'),
    path('bot_wechat_bind_manager', views.bot_wechat_bind_manager, name='bot_wechat_bind_manager'),
    path('bot_wechat_friends', views.bot_wechat_friends, name='bot_wechat_friends'),

    path('check_club_status', views.check_club_status, name='check_club_status'),
    path('orc_add_one', views.orc_add_one, name='orc_add_one'),
    path('deal_img_data', views.deal_img_data, name='deal_img_data'),
]
