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
]