# -*- coding: utf-8 -*-
from django.db import models
import uuid

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class Clubs(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    expired_time = models.DecimalField(max_digits=19, decimal_places=6)
    cost_mode = models.IntegerField(default=0)#抽水模式 固定 还是 百分比
    cost_param = models.CharField(max_length=200, default='none')
    profit = models.IntegerField(default=0)

class Player(models.Model):
    club = models.ForeignKey(Clubs, on_delete=models.CASCADE)
    wechat_id = models.CharField(max_length=200)
    wechat_nick_name = models.CharField(max_length=200)
    nick_name = models.CharField(max_length=200)
    current_score = models.IntegerField(default=0)
    history_profit = models.IntegerField(default=0)
    introducer = models.CharField(max_length=200, default='none')
    today_hoster_number = models.IntegerField(default=0)

class GameID(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game_nick_name = models.CharField(max_length=200)
    gameid = models.CharField(max_length=20)

class Score(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    create_time = models.DateTimeField('create time')
    room_id = models.CharField(max_length=20)

class HistoryGame(models.Model):
    club = models.ForeignKey(Clubs, on_delete=models.CASCADE)
    room_id = models.CharField(max_length=10)
    hoster_name = models.CharField(max_length=20)
    hoster_id = models.IntegerField(default=0)
    round_number = models.IntegerField(default=0)
    start_time = models.CharField(max_length=20)
    player_data = models.CharField(max_length=1000,default='none')#playerResult.playerData的数组
    create_time = models.DateTimeField('create time')

class Cdkey(models.Model):
    cdkey = models.CharField(primary_key=True, max_length=50)
    key_type = models.IntegerField(default=0) #1 -1天，2 - 1周， 3- 1个月
    status = models.IntegerField(default=0)
    create_time = models.IntegerField(default=0)

class WrongImage(models.Model):
    id = models.IntegerField(primary_key=True)
    club_name = models.CharField(max_length=20)
    image = models.CharField(max_length=100)
    create_time = models.IntegerField(default=0)


