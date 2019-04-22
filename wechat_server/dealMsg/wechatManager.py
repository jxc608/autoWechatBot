# -*- coding: utf-8 -*-
import itchat
from itchat.content import *
import time, json, os, datetime, traceback, urllib, urllib.request, ssl
from aip import AipOcr
from DServerAPP.models import *
from . import playerResult
from django.utils import timezone
from django.conf import settings
from django.db.models import F
import threading
import base64, re
import requests
from django.conf import settings

from .statistics import addClubOrcCount, addClubOrcFailCount, addClubOrcRepeatCount

import logging

logger = logging.getLogger(__name__)

# 整数或浮点数皆可
def own_round(foiVal):
    return int(foiVal + 0.5)

# 定义常量
APP_ID = '11756002'
API_KEY = 'FK5TYgAMCPengGGfqbI5GqGz'
SECRET_KEY = 'tGoNHGV0ZuhEVFob1EubxgghoT9B9FPz'

# 初始化文字识别分类器
aipOcr=AipOcr(APP_ID, API_KEY, SECRET_KEY)

# 读取图片
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 定义参数变量
options = {
    'recognize_granularity':'small',
    'detect_direction': 'true',
    'language_type': 'CHN_ENG',
}


def get_aliyun_pic_info(content):
    logger.info(content["sid"])
    infoDic = {}
    keyAry = [
        {"word": "房号", "key": "room_id"},
        {"word": "房主", "key": "hoster"},
        {"word": "局数", "key": "round_number"},
        {"word": "开始时间", "key": "start_time"},
        {"word": "玩家", "key": "name_pos"},
        {"word": "D", "key": "id_pos"},
        {"word": "积分", "key": "score_pos"},
        {"word": "分享", "key": "share"},
    ]

    index = 0
    playerIndex = 0
    data_list = []
    # id下一个不为score，则识别score失败，默认1，同时增加一个
    over_id = False
    for words in content["prism_wordsInfo"]:
        word = words["word"]
        curKey = keyAry[index]
        if index < 7:
            if curKey["word"] in word:
                if index < 4:
                    if(curKey['key'] == 'room_id'):
                        ct = re.sub(r'\D', "", word)
                    else:
                        pattern = "%s(.*)" % curKey["word"]
                        r = re.search(pattern, word, re.M | re.I)
                        ct = r.group(1)
                        # 部分识别不出冒号的问题
                        if ct[0] == ":" or ct[0] == "：":
                            ct = ct[1:]

                    infoDic[curKey["key"]] = ct
                else:
                    infoDic[curKey["key"]] = words["pos"][0]["x"]
                index += 1
        else:
            # 处于识别玩家游戏信息阶段
            if curKey["word"] in word:
                # 终结字段识别
                break
            start = int(words["pos"][0]["x"])
            if playerIndex > len(data_list) - 1:
                data_list.append({})
            if over_id and start < int(infoDic["score_pos"]):
                data_list[playerIndex]["score"] = "1"
                playerIndex += 1
                data_list.append({})
                over_id = False

            if start > int(infoDic["score_pos"]):
                over_id = False
                data_list[playerIndex]["score"] = word
                playerIndex += 1
            elif start > int(infoDic["id_pos"]):
                data_list[playerIndex]["id"] = word
                over_id = True
            elif start > int(infoDic["name_pos"]):
                data_list[playerIndex]["name"] = word

    room_data = playerResult.roomData()
    room_data.roomId = int(infoDic["room_id"])
    room_data.startTime = infoDic["start_time"]
    room_data.roomHoster = infoDic["hoster"].strip()
    room_data.roundCounter = infoDic["round_number"]
    total = 0
    for player in data_list:
        logger.info("内容:\n%s" % player)
        if not "id" in player:
            continue

        p = playerResult.playerData()
        p.name = player.get("name", "")
        p.score = int(player.get("score", "1"))
        p.id = abs(int(player['id']))
        total += abs(p.score)
        room_data.playerData.append(p)
        if p.name.strip() == infoDic["hoster"].strip():
            room_data.roomHosterId = p.id

    score = 0
    for playerData in room_data.playerData:
        if score + abs(playerData.score) > total / 2:
            playerData.score = -abs(playerData.score)
        else:
            playerData.score = abs(playerData.score)
        score += abs(playerData.score)
    room_data.toString()
    return room_data

#itchat 实例列表
_list = {}

class wechatInstance():

    def __init__(self, wid):
        # self.qrid = itchat.get_QRuuid()
        self.login_status = '0'
        self.itchat_instance = itchat.new_instance()
        self.wid = wid

        self.club_name = wid.split("__,__")[0]
        self.club = None

        '''
        接受图片的逻辑处理
        '''
        @self.itchat_instance.msg_register([PICTURE])
        def download_files_new(msg):
            if msg['ToUserName'] != 'filehelper':
                return

            try:
                self.club = Clubs.objects.get(user_name=self.club_name)
            except:
                logger.error("club未找到：" % wid)
                self.send('俱乐部未找到： %s' % self.wid, 'filehelper')
                return
            if self.club.expired_time < time.time():
                self.send('俱乐部已过期： %s， 请与管理员确认' % self.wid, 'filehelper')
                return

            beginStr = "俱乐部：%s，开始识别..." %  self.wid
            logger.info(beginStr)
            self.send("正在识别...", 'filehelper')

            if settings.DEBUG:
                club_path = settings.STATIC_ROOT + '\\upload\\' + self.club.user_name + '\\'
            else:
                club_path = settings.STATIC_ROOT + '/upload/' + self.club.user_name + '/'
            if not os.path.exists(club_path):
                os.mkdir(club_path)
            # logger.info(msg)
            img_file = club_path + msg.get('fileName', msg.get('FileName', int(time.time())))
            msg.download(img_file)
            typeSymbol = {PICTURE: 'img',}.get(msg.type, 'fil')

            erro_msg = ""
            try:
                result = self.get_aliyun_result(img_file)
            except:
                addClubOrcFailCount(self.club)
                erro_msg = '图片无法识别，请试着保存图片或上传原图重新发送，如有疑问请联系管理员'
                self.send_mode_msg(settings.WECHAT_MODE_ONLINE, content=erro_msg, online_user='filehelper')
                # self.itchat_instance.send(erro_msg, 'filehelper')
                return
            self.deal_img_data(settings.WECHAT_MODE_ONLINE, result, fileName=msg.fileName, img_file=img_file)


    def send_mode_msg(self, mode, content='', online_user='', openid='', tm_param={}, is_template=False):
        # content为online模式的文字内容
        # tm_param，内容为{'mediaId':'lastScore', 'roundScore', 'cost', 'currentScore'}
        headers = {'Content-Type': 'application/json'}
        if mode == settings.WECHAT_MODE_ONLINE:
            self.itchat_instance.send(content, online_user)
        elif mode == settings.WECHAT_MODE_SERVICE:
            if is_template:
                postData = {'appid': self.club.appid, 'userid': openid}
                ct = {}
                url = tm_param.get('url', '')
                postData['content'] = {}
                if tm_param['template'] == settings.WECHAT_TEMPLATE_SCORE_ADD[0]:
                    postData['content']['template_id'] = settings.WECHAT_TEMPLATE_SCORE_ADD[1]
                    ct.update(first=tm_param['first'], keyword1=tm_param['keyword1'], keyword2=tm_param['keyword2'],
                        keyword3=tm_param['keyword3'], remark=tm_param['remark'])
                elif tm_param['template'] == settings.WECHAT_TEMPLATE_SCORE_MINUS[0]:
                    postData['content']['template_id'] = settings.WECHAT_TEMPLATE_SCORE_MINUS[1]
                    ct.update(first=tm_param['first'], keyword1=tm_param['keyword1'], keyword2=tm_param['keyword2'],
                              keyword3=tm_param['keyword3'], remark=tm_param['remark'])
                elif tm_param['template'] == settings.WECHAT_TEMPLATE_SCORE_LIMIT[0]:
                    postData['content']['template_id'] = settings.WECHAT_TEMPLATE_SCORE_LIMIT[1]
                    ct.update(first=tm_param['first'], keyword1=tm_param['keyword1'], keyword2=tm_param['keyword2'],
                              remark=tm_param['remark'])
                postData['content']['data'] = ct
                postData['content']['url'] = url
                postData = json.dumps(postData)
                requests.post(settings.WECHAT_TEMPLATE_URL, data=postData, headers=headers)
            else:
                data = {'appid': self.club.appid, 'userid': openid, 'content': content}
                data = json.dumps(data)
                requests.post(settings.WECHAT_TEXT_URL, data=data, headers=headers)

    def deal_img_data(self, mode, aliyun_data, img_url='', media_id='', fromuser='', fileName='', img_file='', club=None):
        if mode == settings.WECHAT_MODE_SERVICE:
            self.club = club
            ct = "俱乐部：%s，开始识别..." %  club.user_name
            self.send_mode_msg(mode, content=ct, online_user='filehelper', openid=fromuser)
        erro_msg = ''
        try:
            room_data = get_aliyun_pic_info(aliyun_data)
        except:
            erro_msg = '图片无法识别，请试着保存图片或上传原图重新发送，如有疑问请联系管理员'

        if erro_msg == "":
            erro_msg = self.scanError(room_data)
        if erro_msg != "":
            # 图片无法识别
            if mode == settings.WECHAT_MODE_SERVICE:
                fileName = media_id
            wrong_image = WrongImage(club_name=self.club.user_name, image=fileName, create_time=int(time.time()))
            wrong_image.save()
            logger.error("club: %s, %s" % (self.wid, "图片识别失败"))
            self.send_mode_msg(mode, content=erro_msg, online_user='filehelper',openid=fromuser)
            # self.itchat_instance.send(erro_msg, 'filehelper')
            return

        existCount = HistoryGame.objects.filter(club=self.club, room_id=room_data.roomId,
                                                start_time=room_data.startTime).count()
        if existCount > 0:
            addClubOrcRepeatCount(self.club)
            logger.error("数据已入库: %s, room_id: %s, start_time: %s" % (self.wid, room_data.roomId, room_data.startTime))
            self.send_mode_msg(mode, content="数据已入库！", online_user='filehelper',openid=fromuser)
            # self.itchat_instance.send('数据已入库！', 'filehelper')
            return

        for num in range(0, len(room_data.playerData)):
            roomPlayData = room_data.playerData[num]
            gi = GameID.objects.filter(club=self.club, gameid=roomPlayData.id, player__is_del=0)
            # 数据库中没有用户，自动增加
            if gi.count() > 1:
                errmsg = '用户id：%s ， 账号名称：%s，匹配到 %s 条，请删除多余的数据后，再上传' % (roomPlayData.id, roomPlayData.name, gi.count())
                logger.error(errmsg)
                self.send_mode_msg(mode, content=errmsg, online_user='filehelper',openid=fromuser)
                # self.itchat_instance.send(errmsg, 'filehelper')
                return

        # 根据刷新时间设置，设置入库时间
        today_time_start = '%s-%s-%s 0:0:0' % (timezone.now().year, timezone.now().month, timezone.now().day)
        timeArray = time.strptime(today_time_start, "%Y-%m-%d %H:%M:%S")
        today_time_start = int(time.mktime(timeArray))

        # 这个刷新时间有什么用？
        refresh_time = timezone.now()
        if time.time() < today_time_start + self.club.refresh_time * 3600:
            refresh_time = timezone.now() - datetime.timedelta(days=1)

        playerData = []
        for d in room_data.playerData:
            playerData.append(d.dumps())
        historyGame = HistoryGame(club=self.club, room_id=room_data.roomId, hoster_name=room_data.roomHoster,
                                  hoster_id=room_data.roomHosterId, round_number=room_data.roundCounter,
                                  start_time=room_data.startTime, player_data=json.dumps(playerData),
                                  refresh_time=refresh_time)
        historyGame.save()
        if self.club.msg_type == 0:
            pic_msg = "房间ID：%s  房主ID：%s\n房主：%s  局数：%s\n开始时间：%s\n" % (
            room_data.roomId, room_data.roomHosterId, room_data.roomHoster, room_data.roundCounter, room_data.startTime)
        else:
            pic_msg = "房间ID：%s\n" % (room_data.roomId)

        rules = []
        if self.club.cost_param != None and self.club.cost_param != 'none' and self.club.cost_param != '':
            rules = self.club.cost_param
            rules = rules.split('|')
        clubProfit = 0

        for num in range(0, len(room_data.playerData)):
            roomPlayData = room_data.playerData[num]
            wechat_uuid = None

            # 获取当前用户的username用来发送消息
            gi = GameID.objects.filter(club=self.club, gameid=roomPlayData.id, player__is_del=0)
            # 数据库中没有用户，自动增加
            if gi.count() == 1:
                player = gi[0].player
            else:
                tm_msg = '用户id：%s 没有注册, 创建临时账号：%s' % (roomPlayData.id, roomPlayData.name)
                self.send_mode_msg(mode, content=tm_msg, online_user='filehelper',openid=fromuser)
                # self.itchat_instance.send(tm_msg, 'filehelper')
                player = self.createTempPlayer(roomPlayData)

            if player.is_bind:
                if mode == settings.WECHAT_MODE_ONLINE:
                    playerWechat = self.getWechatUserByRemarkName(player.nick_name)
                    if playerWechat:
                        wechat_uuid = playerWechat['UserName']
                elif mode == settings.WECHAT_MODE_SERVICE:
                    wechat_uuid = player.openid
            try:
                is_host = 1 if roomPlayData.name == room_data.roomHoster else 0
                if is_host == 1:
                    player.today_hoster_number += 1
                last_current_score = player.current_score
                # 计算管理费
                cost = self.calCostMode(rules, roomPlayData, num)
                score = Score(player=player, score=roomPlayData.score - cost, cost=cost, is_host=is_host,
                              create_time=timezone.now(), room_id=room_data.roomId, refresh_time=refresh_time)
                score.save()
                player.current_score = player.current_score + roomPlayData.score - cost
                player.history_profit = player.history_profit + roomPlayData.score - cost
                player.history_cost += cost
                player.save()
                historyGame.cost += cost
                historyGame.score += roomPlayData.score - cost
                clubProfit += cost

                costShow2 = "本局房费: %s" % cost
                if cost == 0:
                    costShow2 = "本局房费: 无"
                if not cost:
                    cost = 0

                if self.club.msg_type == 0:
                    pic_msg += "%s.-------------------------\n昵称: %s\nID: %s\n上次积分: %s 本局积分: %s\n管理费: %s 当前余分: %s\n" % (
                    num + 1, player.nick_name, roomPlayData.id, last_current_score, roomPlayData.score, cost,
                    player.current_score)
                else:
                    pic_msg += "%s.\n昵称: %s\nID: %s\n上次积分: %s 本局积分: %s\n管理费: %s 当前余分: %s\n" % (
                    num + 1, player.nick_name, roomPlayData.id, last_current_score, roomPlayData.score, cost,
                    player.current_score)
                # pic_msg += str(num + 1) + '.ID' + str(roomPlayData.id) + '：' + player.nick_name + '  分数：' + str(roomPlayData.score) + costShow1 + '  总分数：' + str(player.current_score) + '\n'
                if wechat_uuid:
                    if mode == settings.WECHAT_MODE_ONLINE:
                        self.itchat_instance.send_image(img_file, wechat_uuid)
                        alert_msg = '%s\n上次积分: %s\n本局积分: %s\n%s\n当前余分: %s\n' % (
                            player.nick_name, last_current_score, roomPlayData.score, costShow2, player.current_score)
                        # self.itchat_instance.send(alert_msg, wechat_uuid)
                        self.send_mode_msg(mode, content=alert_msg, online_user=wechat_uuid)
                    elif mode == settings.WECHAT_MODE_SERVICE:
                        tp = settings.WECHAT_TEMPLATE_SCORE_ADD[0]
                        keyword1 = '游戏结算'
                        keyword2 = {'value': '+%s' % roomPlayData.score, 'color': '#00ff00'}
                        if roomPlayData.score < 0:
                            tp = settings.WECHAT_TEMPLATE_SCORE_MINUS[0]
                            keyword2 = {'value': roomPlayData.score, 'color': '#ff0000'}

                        tm_param = {'first': '%s，%s，上次积分：%s' % (player.nick_name, roomPlayData.id, last_current_score),
                                    'keyword1': keyword1, 'template':tp, 'keyword2': keyword2, 'url': img_url,
                                    'keyword3': player.current_score, 'remark': '本局房费：%s' % cost}
                        self.send_mode_msg(mode, tm_param=tm_param, openid=fromuser, is_template=True)

                # 授信检测
                self.scoreLimit(mode, player, wechat_uuid)
            except:
                # traceback.logger.info_exc()
                errmsg = "发生异常：\n姓名: %s\nid: %s\n分数: %s" % (roomPlayData.name, roomPlayData.id, roomPlayData.score)
                logger.error(errmsg)
                self.send_mode_msg(mode, content=erro_msg, online_user='filehelper',openid=fromuser)
                # self.itchat_instance.send(errmsg, 'filehelper')
                continue
        historyGame.save()

        self.club.profit = F("profit") + clubProfit
        self.club.save(update_fields=["profit"])
        if self.club.msg_type == 0:
            pic_msg += '-----------------------------\n'
        # pic_msg+= '获得管理费：%s' % clubProfit
        self.send_mode_msg(mode, content=pic_msg, online_user='filehelper',openid=fromuser)
        # self.itchat_instance.send(pic_msg, 'filehelper')
        # return '@%s@%s' % (typeSymbol, msg.fileName)



    def scanError(self, room_data):
        total_score = 0
        for playerData in room_data.playerData:
            total_score += playerData.score
        erro_msg = ""
        if room_data.startTime == '' or room_data.roomId == 0 or total_score != 0 \
                or room_data.roundCounter == 0 or len(room_data.playerData) == 0 or len(room_data.playerData) > 9:
            erro_msg = '图片无法识别\n'
            erro_msg += 'roomId:%s\n' % room_data.roomId
            erro_msg += 'startTime:%s\n' % room_data.startTime
            erro_msg += 'roomHosterId:%s\n' % room_data.roomHosterId
            erro_msg += 'roomHoster:%s\n' % room_data.roomHoster
            erro_msg += 'roundCounter:%s\n' % room_data.roundCounter
            erro_msg += 'players:%s\n' % len(room_data.playerData)
            erro_msg += 'total_score:%s' % total_score

        return erro_msg

    def createTempPlayer(self, roomPlayData):
        player = Player(wechat_nick_name=roomPlayData.name, nick_name=roomPlayData.name, club=self.club, current_score=0, history_profit=0)
        player.save()
        gameid = GameID(club=self.club, player=player, gameid=roomPlayData.id, game_nick_name=roomPlayData.name)
        gameid.save()
        return player

    def scoreLimit(self, mode, player, wechat_uuid):
        if player.score_limit != 0 and player.current_score <= -player.score_limit:
            if mode == settings.WECHAT_MODE_ONLINE:
                alert_msg = player.nick_name + '\n'
                alert_msg += '上分提醒\n'
                alert_msg += '当前余分: %s\n' % player.current_score
                alert_msg += player.score_limit_desc + '\n'
                alert_msg += '本条消息来自傻瓜机器人自动回复\n'
            elif mode == settings.WECHAT_MODE_SERVICE:
                alert_msg = {'first': '%s 上分提醒' % player.nick_name, 'keyword1': '当前余分: %s' % player.current_score,
                    'keyword2': player.score_limit_desc, 'remark': '%s\n本条消息来自傻瓜机器人自动回复' % player.score_limit_desc,
                             'template': settings.WECHAT_TEMPLATE_SCORE_LIMIT[0]}

            if player.is_bind and wechat_uuid:
                self.send_mode_msg(mode, content=alert_msg, tm_param=alert_msg, online_user=wechat_uuid, is_template=True)
                # self.itchat_instance.send(alert_msg, wechat_uuid)

            # 管理员
            manager_wechat_uuids = []
            if mode == settings.WECHAT_MODE_ONLINE:
                for manager in Manager.objects.filter(club=self.club):
                    f = self.itchat_instance.search_friends(name=manager.nick_name)
                    if f:
                        if isinstance(f, list):
                            manager_wechat_uuids.append(f[0]['UserName'])
                        elif isinstance(f, dict):
                            manager_wechat_uuids.append(f['UserName'])
                for manager_wechat_uuid in manager_wechat_uuids:
                    self.send_mode_msg(mode, content=alert_msg, online_user=manager_wechat_uuid)

            elif mode == settings.WECHAT_MODE_SERVICE :
                for manager in Manager.objects.filter(club=self.club):
                    if manager.openid:
                        self.send_mode_msg(mode, tm_param=alert_msg, openid=manager.openid, is_template=True)

                # self.itchat_instance.send(alert_msg, manager_wechat_uuid)

    def calCostMode(self, rules, roomPlayData, num):
        cost = 0
        if len(rules) > 0:
            costMode = self.club.cost_mode
            if costMode == 0 and num < int(rules[0]):
                value = int(rules[2])
                params = rules[1].split('_')

                if roomPlayData.score > value:
                    # 超过分数才计算
                    if type(eval(params[num])) == int:
                        cost = own_round(float(params[num]))
                    elif type(eval(params[num])) == float:
                        cost = own_round(roomPlayData.score * float(params[num]))
            elif costMode == 1 and num < int(rules[0]):
                ranges = rules[1].split('*')
                costs = rules[2].split('*')
                for index, range_ in enumerate(ranges):
                    if num == index:
                        costs_ = costs[index].split('_')
                        for rindex, rrange_ in enumerate(range_.split('_')):
                            if roomPlayData.score < int(rrange_):
                                cost = own_round(float(costs_[rindex]))
                                break
                if cost <= 0:
                    cost = 0
            elif costMode == 2:
                values = rules[0].split('_')
                costs = rules[1].split('_')
                can_cost = False
                for index, value in enumerate(values):
                    if roomPlayData.score >= int(value):
                        can_cost = True
                        break
                # 所有固定模式
                if can_cost:
                    cost = own_round(float(costs[index]))
        return abs(cost)

    def get_aliyun_result(self, img_file):
        '''
       阿里云识别
       '''
        host = 'https://ocrapi-advanced.taobao.com'
        path = '/ocrservice/advanced'
        method = 'POST'
        appcode = 'a0ce79e60fc1405d8032b38dbb51f479'
        url = host + path

        post_data = {"img": str(base64.b64encode(get_file_content(img_file)), "utf-8")}
        post_data = json.dumps(post_data).encode("utf-8")
        request = urllib.request.Request(url, post_data, method=method)
        request.add_header('Authorization', 'APPCODE ' + appcode)
        request.add_header('Content-Type', 'application/json; charset=UTF-8')
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        response = urllib.request.urlopen(request, context=ctx)
        result = response.read()
        result = json.loads(result)

        addClubOrcCount(self.club)
        return result

    @staticmethod
    def new_instance(wid):
        if not _list.get(wid):
            _list[wid] = wechatInstance(wid)
        return _list[wid]

    @staticmethod
    def logoutAll():
        for key in _list:
            _list[key].logout()

    def refresh_uuid(self):
        status, _ = self.check_login_status()
        uuid = ''
        if status != '200':
            uuid = self.itchat_instance.get_QRuuid()
            self.check_login(uuid)
        return uuid


    def check_login(self, uuid):
        def check():
            success = False
            while 1:
                status = self.itchat_instance.check_login(uuid)
                if status == '200':
                    success = True
                    break
                elif status == '201':
                    pass
                elif status == '408':
                    break
                elif status == '400':
                    logger.error("uuid: %s, club：%s, 该环境暂时不能登录web微信" % (uuid, self.wid))
                    break
                time.sleep(1)

            if success:
                userInfo = self.itchat_instance.web_init()
                self.itchat_instance.show_mobile_login()
                self.itchat_instance.get_contact(update=True)
                self.itchat_instance.start_receiving()
                self.itchat_instance.run(debug=False, blockThread=False)
                logger.info('uuid: %s, club：%s, Login successfully as %s' % (uuid, self.wid, userInfo['User']['NickName']))

        t = threading.Thread(target=check)
        t.start()


    def check_login_status(self):
        status = '200' if self.itchat_instance.alive else '0'
        desc = ''
        return status, desc
        # return self.itchat_instance.alive
        # status = self.login_status
        # desc = ""
        # if status == '201':
        #     desc = "等待扫码确认"
        # if status == '408':
        #     desc = "二维码已失效，请刷新后重试"
        # elif status == '400':
        #     desc = "该环境暂时不能登录web微信"
        # elif status == '200':
        #     if not self.itchat_instance.alive:
        #         status = '0'
        # return status, desc


    def logout(self):
        logger.info("用户退出登录: %s" % self.wid)
        self.itchat_instance.logout()

    def sendByRemarkName(self, msg, remarkName):
        f = self.getWechatUserByRemarkName(remarkName=remarkName)
        if f:
            f.send(msg)

    def send(self, msg, user_name):
        self.itchat_instance.send(msg, user_name)

    def getWechatUserByRemarkName(self, remarkName):
        user = None
        f = self.itchat_instance.search_friends(name=remarkName)
        if f:
            if isinstance(f, list):
                user = f[0]
            elif isinstance(f, dict):
                user = f
        return user

    def search_friends(self, name):
        list_ = []
        f = self.itchat_instance.search_friends(name=name)

        if isinstance(f,list):
            for ff in f:
                data = {
                    "NickName":ff["NickName"],
                    "UserName":ff["UserName"],
                    "RemarkName": ff["RemarkName"],
                    "Signature":ff["Signature"],
                    "HeadImgUrl":ff["HeadImgUrl"],
                }
                list_.append(data)
        elif isinstance(f,dict):
            data = {
                "NickName":f["NickName"],
                "UserName":f["UserName"],
                "RemarkName": f["RemarkName"],
                "Signature":f["Signature"],
                "HeadImgUrl":f["HeadImgUrl"],
            }
            list_.append(data)

        return list_

    def set_alias(self, wechat_user_name, nick_name):
        ret = self.itchat_instance.set_alias(wechat_user_name, nick_name)
        if ret['BaseResponse']['Ret'] != 0:
            return 2, ret['BaseResponse']['ErrMsg']
        return 0, '绑定成功'


