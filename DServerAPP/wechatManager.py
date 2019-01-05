# -*- coding: utf-8 -*-
import itchat
from itchat.content import *
import time, json, os, datetime, traceback, re, urllib, urllib.request, ssl
from aip import AipOcr
from .models import *
from . import playerResult
from django.utils import timezone
from django.conf import settings
from django.db.models import F
from .utils import *
import _thread
import base64

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

def output_info(msg):
    print('[INFO] %s' % msg)

def addClubOrcCount(club):
    if club == None:
        print("跟同学统计次数，俱乐部为空")
        return
    curDate = datetime.datetime.now().date()
    try:
        ct = ClubOrcCount.objects.get(club=club, use_date=curDate)
    except ClubOrcCount.DoesNotExist:
        print("新建统计记录__%s__%s" % (club.user_name, curDate))
        ct = ClubOrcCount(club=club, use_date=curDate)
        ct.save()
    except:
        print("更新统计次数失败，错误未知")
        traceback.print_exc()
        return
    ct.count = F("count") + 1
    ct.save()


def get_aliyun_pic_info(content):
    print(content["sid"])
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
    room_data.roomId = infoDic["room_id"]
    room_data.startTime = infoDic["start_time"]
    room_data.roomHoster = infoDic["hoster"].strip()
    room_data.roundCounter = infoDic["round_number"]
    total = 0
    for player in data_list:
        print("内容:\n%s" % player)
        if not "id" in player:
            continue

        p = playerResult.playerData()
        p.name = player.get("name", "")
        p.score = int(player.get("score", "1"))
        p.id = int(player['id'])
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

    def __init__(self, clubName):
        # self.qrid = itchat.get_QRuuid()
        self.logined = False
        self.itchat_instance = itchat.new_instance()
        self.club_name = clubName
        self.club = None
        try:
            self.club = Clubs.objects.get(user_name=clubName)
        except:
            print("club未找到：" % clubName)

        '''
        接受图片的逻辑处理
        '''
        @self.itchat_instance.msg_register([PICTURE])
        def download_files_new(msg):
            if msg['ToUserName'] != 'filehelper':
                return
            if self.club == None:
                self.send('俱乐部未找到： %s' % self.club_name, 'filehelper')
                return
            elif self.club.expired_time < time.time():
                self.send('俱乐部已过期： %s， 请与管理员确认' % self.club_name, 'filehelper')
                return

            beginStr = "俱乐部：%s，开始识别..." %  self.club.user_name
            output_info(beginStr)
            self.send("正在识别...", 'filehelper')

            club_path = settings.STATIC_ROOT + '/upload/' + self.club.user_name + '/'
            if not os.path.exists(club_path):
                os.mkdir(club_path)
            img_file = club_path + msg.fileName
            msg.download(img_file)
            typeSymbol = {PICTURE: 'img',}.get(msg.type, 'fil')

            erro_msg = ""
            try:
                result = self.get_aliyun_result(img_file)
                room_data = get_aliyun_pic_info(result)
            except:
                erro_msg = '图片无法识别\n请试着上传原图，或者联系管理员'
            if erro_msg == "":
                erro_msg = self.scanError(room_data)
            if erro_msg != "":
                # 图片无法识别
                wrong_image = WrongImage(club_name=self.club.user_name, image=msg.fileName, create_time=int(time.time()))
                wrong_image.save()
                self.itchat_instance.send(erro_msg, 'filehelper')
                print(erro_msg)
                return

            existCount = HistoryGame.objects.filter(club=self.club, room_id=room_data.roomId, start_time=room_data.startTime).count()
            if existCount > 0:
                self.itchat_instance.send('数据已入库！', 'filehelper')
                return

            #根据刷新时间设置，设置入库时间
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
            historyGame = HistoryGame(club=self.club, room_id=room_data.roomId, hoster_name=room_data.roomHoster,hoster_id=room_data.roomHosterId, round_number=room_data.roundCounter, start_time=room_data.startTime, player_data=json.dumps(playerData), refresh_time=refresh_time)
            historyGame.save()
            pic_msg = "房间ID：%s  房主ID：%s\n房主：%s  局数：%s\n开始时间：%s\n" % (room_data.roomId, room_data.roomHosterId, room_data.roomHoster,room_data.roundCounter, room_data.startTime)
            # pic_msg += "-----------------------------\n"

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
                if gi.count() > 1:
                    self.itchat_instance.send('用户id：%s ， 账号名称：%s，匹配到 %s 条，请删除多余的数据后，再上传' % (roomPlayData.id, roomPlayData.name, giCount),'filehelper')
                    return
                elif gi.count() == 1:
                    player = gi[0].player
                else:
                    self.itchat_instance.send('用户id：%s 没有注册, 创建临时账号：%s' % (roomPlayData.id, roomPlayData.name), 'filehelper')
                    player = self.createTempPlayer(roomPlayData)
                    playerWechat = self.getWechatUserByRemarkName(player.nick_name)
                    if playerWechat:
                        wechat_uuid = playerWechat['UserName']

                try:
                    is_host = 1 if roomPlayData.name == room_data.roomHoster else 0
                    if is_host == 1:
                        player.today_hoster_number += 1
                    last_current_score = player.current_score
                    # 计算管理费
                    cost = self.calCostMode(rules, roomPlayData, num)
                    score = Score(player=player, score=roomPlayData.score - cost, cost=cost, is_host=is_host, create_time=timezone.now(), room_id=room_data.roomId, refresh_time=refresh_time)
                    score.save()
                    player.current_score = player.current_score + roomPlayData.score - cost
                    player.history_profit = player.history_profit + roomPlayData.score - cost
                    player.history_cost += cost
                    player.save()
                    historyGame.cost += cost
                    historyGame.score += roomPlayData.score - cost
                    clubProfit += cost
                    costShow1 = "管理费： %s\n" % cost
                    costShow2 = "  本局房费: %s" % cost
                    if cost == 0:
                        costShow1 = ""
                        costShow2 = "  本局房费: 无"
                    pic_msg += "%s.-------------------------\n昵称：%s  ID：%s\n分数：%s  总分数：%s\n%s" % (num + 1, player.nick_name, roomPlayData.id, roomPlayData.score, player.current_score, costShow1)
                    pic_msg += str(num + 1) + '.ID' + str(roomPlayData.id) + '：' + player.nick_name + '  分数：' + str(roomPlayData.score) + costShow1 + '  总分数：' + str(player.current_score) + '\n'
                    if wechat_uuid != None:
                        self.itchat_instance.send_image(img_file, wechat_uuid)
                        alert_msg = '%s\n上次积分: %s\n本局积分: %s\n%s\n当前余分: %s\n' % (player.nick_name, last_current_score, roomPlayData.score, costShow2, player.current_score)
                        self.itchat_instance.send(alert_msg, wechat_uuid)

                        #授信检测
                        self.scoreLimit(player, wechat_uuid)
                except:
                    traceback.print_exc()
                    errmsg = "发生异常：\n姓名: %s\nid: %s\n分数: %s" % (roomPlayData.name, roomPlayData.id, roomPlayData.score)
                    print(errmsg)
                    self.itchat_instance.send(errmsg, 'filehelper')
                    continue
            historyGame.save()
          
            self.club.profit += clubProfit
            self.club.save()
            pic_msg+= '-----------------------------\n'
            pic_msg+= '获得管理费：%s' % clubProfit
            self.itchat_instance.send(pic_msg, 'filehelper') 
            return '@%s@%s' % (typeSymbol, msg.fileName)

    @classmethod
    def new_instance(cls, club):
        if not _list.get(club): 
            _list[club] = wechatInstance(club)
        return _list[club]

    @classmethod
    def check_alive(self, club):
        if _list.get(club) and _list.get(club).itchat_instance.alive:
            return True
        else:
            return False

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

    def scoreLimit(self, player, wechat_uuid):
        if player.current_score <= -player.score_limit:
            alert_msg = player.nick_name + '\n'
            alert_msg += '上分提醒\n'
            alert_msg += '当前余分: %s\n' % player.current_score
            alert_msg += player.score_limit_desc + '\n'
            alert_msg += '本条消息来自傻瓜机器人自动回复\n'
            self.itchat_instance.send(alert_msg, wechat_uuid)

            # 管理员
            manager_wechat_uuids = []
            for manager in Manager.objects.filter(club=self.club):
                f = self.itchat_instance.search_friends(remarkName=manager.nick_name)
                if f:
                    if isinstance(f, list):
                        manager_wechat_uuids.append(f[0]['UserName'])
                    elif isinstance(f, dict):
                        manager_wechat_uuids.append(f['UserName'])
            for manager_wechat_uuid in manager_wechat_uuids:
                self.itchat_instance.send(alert_msg, manager_wechat_uuid)

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
                        cost = int(params[num])
                    elif type(eval(params[num])) == float:
                        cost = round(roomPlayData.score * float(params[num]))
            elif costMode == 1 and num < int(rules[0]):
                ranges = rules[1].split('*')
                costs = rules[2].split('*')
                for index, range_ in enumerate(ranges):
                    if num == index:
                        costs_ = costs[index].split('_')
                        for rindex, rrange_ in enumerate(range_.split('_')):
                            if roomPlayData.score < int(rrange_):
                                cost = int(costs_[rindex])
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
                    cost = int(costs[index])
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

    def is_login(self):
        return self.logined
        # if self.itchat_instance.alive:
        #     return True
        # else:
        #     return False

    def get_uuid(self):
        return self.itchat_instance.get_QRuuid()

    def check_login(self, uuid):
        success = False
        while 1:
            status = self.itchat_instance.check_login(uuid)
            if status == '200':
                success = True
                break
            elif status == '201':
                # 等待确认
                time.sleep(1)
                output_info("wait for confirm: wechat login")
            elif status == '408':
                # 二维码失效
                output_info('Please Reloading QR Code')
                break
        if success:
            # 失效判断，应该在登录的一瞬间自动判断，然后失效则发送消息后，自动注销
            if self.club.expired_time < time.time():
                self.send('CD KEY 已失效。 请延长后继续使用。', 'filehelper')
                self.logout()
            else:
                userInfo = self.itchat_instance.web_init()
                self.itchat_instance.show_mobile_login()
                self.itchat_instance.get_contact(update=True)
                output_info('Login successfully as %s' % userInfo['User']['NickName'])
                self.itchat_instance.start_receiving()
                self.logined = True
                _thread.start_new_thread(self.itchat_instance.run, ())

    def logout(self):
        self.logined = False
        self.itchat_instance.logout()

    def sendByRemarkName(self, msg, remarkName):
        f = self.getWechatUserByRemarkName(remarkName=remarkName)
        if f:
            f.send(msg)

    def send(self, msg, user_name):
        self.itchat_instance.send(msg, user_name)

    def getWechatUserByRemarkName(self, remarkName):
        user = None
        f = self.itchat_instance.search_friends(remarkName=remarkName)
        if f:
            if isinstance(f, list):
                user = f[0]
            elif isinstance(f, dict):
                user = f
        return user

    def search_friends(self, wechat_nick_name, remarkName):
        list_ = []
        has_nickname = []
        f = self.itchat_instance.search_friends(nickName=wechat_nick_name)

        if isinstance(f,list):
            for ff in f:
                data = {
                    "NickName":ff["NickName"],
                    "UserName":ff["UserName"],
                    "Signature":ff["Signature"],
                    "HeadImgUrl":ff["HeadImgUrl"],
                }
                has_nickname.append(ff["NickName"])
                list_.append(data)
        elif isinstance(f,dict):
            data = {
                "NickName":f["NickName"],
                "UserName":f["UserName"],
                "Signature":f["Signature"],
                "HeadImgUrl":f["HeadImgUrl"],
            }
            has_nickname.append(f["NickName"])
            list_.append(data)

        f = self.itchat_instance.search_friends(remarkName=remarkName)
        if isinstance(f,list):
            for ff in f:
                if ff["NickName"] not in has_nickname:
                    data = {
                        "NickName":ff["NickName"],
                        "UserName":ff["UserName"],
                        "Signature":ff["Signature"],
                        "HeadImgUrl":ff["HeadImgUrl"],
                    }
                    list_.append(data)
        elif isinstance(f,dict):
            if f["NickName"] not in has_nickname:
                data = {
                    "NickName":f["NickName"],
                    "UserName":f["UserName"],
                    "Signature":f["Signature"],
                    "HeadImgUrl":f["HeadImgUrl"],
                }
                has_nickname.append(f["NickName"])
                list_.append(data)

        return list_

    def set_alias(self, wechat_user_name, nick_name):
        ret = self.itchat_instance.set_alias(wechat_user_name, nick_name)
        if ret['BaseResponse']['Ret'] != 0:
            return 2, ret['BaseResponse']['ErrMsg']
        return 0, '绑定成功'


