from django.urls import path

from . import views

urlpatterns = [
    path('login', views.index, name='index'),
    path('registerPage', views.registerPage, name='registerPage'),
    path('register', views.register, name='register'),
    path('login_password', views.login_password, name='login_password'),
    path('login_smscode', views.login_smscode, name='login_smscode'),
    path('bind_wechat', views.bind_wechat, name='bind_wechat'),
]