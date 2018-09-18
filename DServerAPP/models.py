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
    expired_time = models.DateTimeField('expired Time')

class Player(models.Model):
    club = models.ForeignKey(Clubs, on_delete=models.CASCADE)
    wechat_id = models.CharField(max_length=200)
    wechat_nick_name = models.CharField(max_length=50)
    current_Score = models.CharField(max_length=20)

class GameID(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game_nick_name = models.CharField(max_length=200)
    gameid = models.CharField(max_length=20)

class Score(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    create_time = models.DateTimeField('create time')
    room_id = models.CharField(max_length=20)



