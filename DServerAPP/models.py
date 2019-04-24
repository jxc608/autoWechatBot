# -*- coding: utf-8 -*-
from django.db import models
import uuid
from django.utils import timezone

USE_STATUS = [(0,"未使用"), (1, "已使用")]
CDKEY_TYPE = [(1, "一天"), (2, "一周"), (3, "一个月")]
COST_MODE = [(0, '前x名固定或百分比'), (1, '前x名范围'), (2, '所有固定')]
IS_HOST = [(0, '不是'), (1, '是')]
YES_NO_GENERATE = [(0, '否'), (1, '是')]
MSG_TYPE = [(0, '微信'), (1, '默往')]

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name="问题内容")
    pub_date = models.DateTimeField(verbose_name="发布时间")

    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name = "问题"
        verbose_name_plural = verbose_name


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="问题")
    choice_text = models.CharField(max_length=200, verbose_name="选择")
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

    class Meta:
        verbose_name = "选择"
        verbose_name_plural = verbose_name

class Clubs(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='uuid')
    user_name = models.CharField(max_length=20, verbose_name='名称')
    password = models.CharField(max_length=20, verbose_name='密码')
    password2 = models.CharField(max_length=20, verbose_name='二级密码', default='')
    expired_time = models.DecimalField(max_digits=19, decimal_places=6, verbose_name='过期时间')
    cost_mode = models.IntegerField(default=0, choices=COST_MODE, verbose_name='管理模式')#管理费模式 固定 还是 百分比
    cost_param = models.CharField(max_length=1000, default='none', verbose_name='管理费参数')
    profit = models.IntegerField(default=0, verbose_name='利润')
    msg_type = models.SmallIntegerField(default=0, choices=MSG_TYPE, verbose_name="消息格式", null=False)
    # 该字段暂时没用？
    refresh_time = models.IntegerField(default=0, verbose_name='每天几点刷新数据，暂时无用')
    appid = models.CharField(max_length=32, verbose_name="微信appid", blank=True, default="", unique=True)

    def __str__(self):
        return self.user_name

    def __unicode__(self):
        return self.user_name.encode('utf8')

    class Meta:
        verbose_name = "俱乐部"
        verbose_name_plural = verbose_name

class Captain(models.Model):
    name = models.CharField(max_length=100, verbose_name="队长")
    club = models.ForeignKey(Clubs, on_delete=models.CASCADE, verbose_name="俱乐部")

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name.encode('utf8')

    class Meta:
        verbose_name = "队长信息"
        verbose_name_plural = verbose_name

class ClubOrcCount(models.Model):
    club = models.ForeignKey(Clubs, on_delete=models.CASCADE, verbose_name="俱乐部")
    use_date = models.DateField(default='', verbose_name='使用日期')
    count = models.IntegerField(default=0, verbose_name='使用次数')
    repeat_count = models.IntegerField(default=0, verbose_name='重复次数')
    fail_count = models.IntegerField(default=0, verbose_name='失败次数')

    def __str__(self):
        return "%s_%s_%s" % (self.club.user_name, self.use_date, self.count)

    class Meta:
        verbose_name = "图像识别次数"
        verbose_name_plural = verbose_name

class Player(models.Model):
    club = models.ForeignKey(Clubs, on_delete=models.CASCADE, verbose_name="俱乐部")
    wechat_id = models.CharField(max_length=200, verbose_name="微信ID")
    wechat_nick_name = models.CharField(max_length=200, verbose_name="微信昵称")
    # 备注昵称，绑定时，会同时更新到微信的remarkName【微信昵称本身绑定时作为第一匹配条件，remarkName第二匹配】
    nick_name = models.CharField(max_length=200, verbose_name="备注昵称", default='')
    current_score = models.IntegerField(default=0, verbose_name="当前分数")
    history_profit = models.IntegerField(default=0, verbose_name="总利润/战绩？")
    history_cost = models.IntegerField(default=0, verbose_name="总管理费")
    introducer = models.ForeignKey(Captain, on_delete=models.SET_NULL, null=True, verbose_name='队长', blank=True)
    today_hoster_number = models.IntegerField(default=0, verbose_name="今日开房次数")
    score_limit = models.IntegerField(default=0, verbose_name="分数上限")
    score_limit_desc = models.CharField(max_length=500, verbose_name="授信", default='', blank=True)
    is_del = models.IntegerField(default=0, choices=YES_NO_GENERATE, verbose_name="是否删除")
    is_bind = models.IntegerField(default=0, choices=YES_NO_GENERATE, verbose_name="是否绑定")
    openid = models.CharField(max_length=32, verbose_name="微信openid", blank=True, default='')
    qrcode_url = models.URLField(verbose_name="权限二维码", null=True, blank=True, default=None)

    def __str__(self):
        return  self.nick_name

    class Meta:
        verbose_name = "玩家信息"
        verbose_name_plural = verbose_name

class PlayerClearCost(models.Model):
    # player_id_orgin = models.IntegerField(default=0)
    player = models.ForeignKey(Player, verbose_name="玩家",on_delete=models.CASCADE, null=True)
    history_cost = models.IntegerField(default=0, verbose_name="管理费")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "玩家管理费清理记录"
        verbose_name_plural = verbose_name

class GameID(models.Model):
    #一个俱乐部中的某用户，在game图片中的id对应
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name="用户")
    club = models.ForeignKey(Clubs, on_delete=models.CASCADE, verbose_name="俱乐部", default='')
    game_nick_name = models.CharField(max_length=200, verbose_name="游戏中昵称")
    gameid = models.CharField(max_length=20, verbose_name="图片中的playerid")

    class Meta:
        verbose_name = "玩家游戏信息"
        verbose_name_plural = verbose_name

class Score(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name="玩家")
    score = models.IntegerField(default=0, verbose_name="得分")
    cost = models.IntegerField(default=0, verbose_name="管理费")
    is_host = models.IntegerField(default=0, choices=IS_HOST, verbose_name="是否是房主")
    create_time = models.DateTimeField(verbose_name="创建时间")
    room_id = models.IntegerField(verbose_name="房间ID")
    refresh_time = models.DateTimeField(verbose_name="最近更新时间", default=timezone.now)

    class Meta:
        verbose_name = "得分记录"
        verbose_name_plural = verbose_name

class HistoryGame(models.Model):
    club = models.ForeignKey(Clubs, on_delete=models.CASCADE, verbose_name="俱乐部")
    room_id = models.IntegerField(verbose_name="房间号")
    hoster_name = models.CharField(max_length=20, verbose_name="主机名称", default='')
    hoster_id = models.IntegerField(default=0, verbose_name="主机ID")
    round_number = models.IntegerField(default=0, verbose_name="对局数，游戏几局几胜？")
    start_time = models.CharField(max_length=20, verbose_name="游戏开始时间")
    player_data = models.CharField(max_length=1000,default='', verbose_name="游戏数据")
    create_time = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    cost = models.IntegerField(default=0, verbose_name="管理费")
    score = models.IntegerField(default=0, verbose_name="得分")
    refresh_time = models.DateTimeField(verbose_name="最近刷新时间", default=timezone.now)

    def __str__(self):
        return "%s_%s" % (self.room_id, self.start_time)

    class Meta:
        verbose_name = "游戏历史记录"
        verbose_name_plural = verbose_name

        unique_together = ('club', 'room_id', 'start_time')

class HistoryGameClearCost(models.Model):
    # history_id_orgin = models.IntegerField(default=0)
    history = models.ForeignKey(HistoryGame, verbose_name="历史记录", on_delete=models.CASCADE, null=True)
    cost = models.IntegerField(default=0, verbose_name="管理费")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "游戏记录管理费清理"
        verbose_name_plural = verbose_name

class Cdkey(models.Model):
    cdkey = models.CharField(primary_key=True, max_length=50, verbose_name="密钥")
    club = models.ForeignKey(Clubs, on_delete=models.CASCADE, verbose_name="俱乐部", default=None, null=True, blank=True)
    key_type = models.IntegerField(default=0, choices=CDKEY_TYPE, verbose_name="密钥类型") #1 -1天，2 - 1周， 3- 1个月
    status = models.IntegerField(default=0, choices=USE_STATUS, verbose_name="使用状态")
    create_time = models.IntegerField(default=0, verbose_name="创建时间")
    use_time = models.DateTimeField(null=True, verbose_name="使用时间")

    class Meta:
        verbose_name = "Cdkey"
        verbose_name_plural = verbose_name

class WrongImage(models.Model):
    club_name = models.CharField(max_length=20, verbose_name="俱乐部")
    image = models.CharField(max_length=100, verbose_name="图片")
    create_time = models.IntegerField(default=0, verbose_name="创建时间")

    def __str__(self):
        return self.club_name

    class Meta:
        verbose_name = "错误图片"
        verbose_name_plural = verbose_name

class ScoreChange(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name="玩家")
    score = models.IntegerField(default=0, verbose_name="分数变化值")
    agent = models.CharField(max_length=500, verbose_name="客户端")
    ip = models.CharField(max_length=20, verbose_name="IP")
    create_time = models.IntegerField(default=0, verbose_name="创建时间")

    class Meta:
        verbose_name = "分数手动修改"
        verbose_name_plural = verbose_name

class Manager(models.Model):
    #只有管理员才能上传图片？
    club = models.ForeignKey(Clubs, on_delete=models.CASCADE, verbose_name="俱乐部")
    wechat_nick_name = models.CharField(max_length=200, verbose_name="微信昵称")
    nick_name = models.CharField(max_length=200, verbose_name="备注昵称")
    openid = models.CharField(max_length=32, verbose_name="微信openid", blank=True, default='')
    create_time = models.IntegerField(default=0, verbose_name="创建时间")
    qrcode_url = models.URLField(verbose_name="权限二维码", null=True, blank=True, default=None)

    class Meta:
        verbose_name = "管理员"
        verbose_name_plural = verbose_name



