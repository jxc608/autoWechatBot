# -*- coding: utf-8 -*-
import itchat
from itchat.content import *
import time, json, os, datetime, traceback, re
import threading
from aip import AipOcr
from .models import *
from . import playerResult
from django.utils import timezone
from django.db import connection
from django.conf import settings

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

def getCloseAnchor(map, Anchor, height):
    for key in map:
        if abs(Anchor - key) <= (height / 2):
            return key
    return 0
#lock = threading.Lock()

def createQuadList(item):
    quadList = []
    quadList.append(createCQ(item))
    return quadList

def createCQ(item):
    cq = playerResult.contentQuad()
    cq.words = item['words']
    cq.chars = item['chars']
    cq.leftAnchor = item['chars'][0]['location']['left']
    return cq

def getSortedDict(dict):
    keys = dict.keys() 
    keys.sort() 
    return [dict[key] for key in keys] 

# def getRoomIDAndHoster(rowData, index):
#     print('walawala===='+rowData[index].words)
#     roomId = 0
#     hoster = ''
#     flag1 = rowData[index].words.find(':')
#     rawId = rowData[index].words[flag1 + 1:].strip().replace(' ','')
#
#     if rawId.isdigit():
#         roomId = int(rawId)
#     else:
#         numberList = []
#         for char in rawId:
#             if char.isdigit():
#                 numberList.append(int(char))
#                 print(char)
#             else:
#                 print('fuck:' + char)
#
#         length = len(numberList)
#         roomId = 0
#         for num in range(0, len(numberList)):
#             roomId += numberList[num] * pow(10, length - num - 1)
#     print('the roomId is:' + str(roomId))
#     flag2 = rowData[index + 1].words.find(':')
#     hoster = rowData[index + 1].words[flag2 + 1:]
#     return roomId, hoster

# def getRoundNumberAndStartTime(rowData):
#     roundNumber = 0
#     idLeftPos = 0
#     startTime = ''
#     flag1 = rowData[0].words.find(':')
#     print('the round number string is:' + rowData[0].words[flag1 + 1:])
#     roundNumber = int(rowData[0].words[flag1 + 1:])
#     print('the new round nubmer is:' + str(roundNumber))
#     flag2 = rowData[1].words.find(':')
#     startTime = rowData[1].words[flag2 + 1:]
#     if '开' in rowData[1].words:
#         index = rowData[1].words.find('开')
#         idLeftPos = int(rowData[1].chars[index]['location']['left']) + int(rowData[1].chars[index]['location']['width']) + 13
#     if '始' in rowData[1].words:
#         index = rowData[1].words.find('始')
#         idLeftPos = int(rowData[1].chars[index]['location']['left'])
#     if '时' in rowData[1].words:
#         index = rowData[1].words.find('时')
#         idLeftPos = int(rowData[1].chars[index]['location']['left']) - int(rowData[1].chars[index]['location']['width']) - 26
#     if '间' in rowData[1].words:
#         index = rowData[1].words.find('间')
#         idLeftPos = int(rowData[1].chars[index]['location']['left']) - int(rowData[1].chars[index]['location']['width']) * 2 - 26
#     return roundNumber, startTime, idLeftPos

# def updatePlayerScore(gameid, score):
#     try:
#         gameID = GameID.objects.get(gameid=gameid)
#         return 0
#     except GameID.DoesNotExist:
#         return -1

# def getPlayerScore(nickName, itchatInstance, self):
#     try:
#         player = Player.objects.get(wechat_nick_name=nickName, club=self.club)
#         itchatInstance.send('用户当前分数：' + str(player.current_score) + \
#         '用户历史战绩：' + str(player.history_profit), 'filehelper')
#     except Player.DoesNotExist:
#         itchatInstance.send('用户:' + nickName + '不存在，请先注册用户', 'filehelper')
#         return '命令执行失败: %s' % msg['Content']

# def get_data_pos(index, result):
#     pos = {}
#     pos = []
#     for i, words in enumerate(result):
#         if i <= index:
#             continue
#         left = words['chars'][0]['location']['left']
#         pos.append(left)
#     pos.sort()
#     print(pos)

def get_pic_info(result):
    print(result)
    room_id = 0
    hoster = None
    hoster_id = 0
    round_number = 0
    start_time = None

    caption_user = False
    caption_id = False
    caption_score = False

    player = None
    player_id = None
    score = None

    player_chars = None
    player_id_chars = None
    score_chars = None
    #标题开始标志
    caption_start = False
    #玩家信息开始标志
    player_start = False
    #首字范围
    pos_range = {
        'player':{'start':200, 'end':300, 'base':139},
        'player_id':{'start':600, 'end':650, 'base':612},
        'score':{'start':790, 'end':850, 'base':796},
    }
    player_pos = 0
    data_list = []
    for index, words in enumerate(result):
        if not room_id:
            r = re.search(r'房号:\d+', words['words'])
            if r:
                room_id = int(r.group(0).split(':')[1])
        if not hoster:
            r = re.search(r'房主:(.*)', words['words'])
            if r:
                hoster = r.group(0).split(':')[1]
            r = re.search(r'房主$', words['words'])
            if r:
                hoster = '-'
        if not round_number:
            r = re.search(r'局数:\d+', words['words'])
            if r:
                round_number = int(r.group(0).split(':')[1])
        if not start_time:
            r = re.search(r'开始时间:(.*)', words['words'])
            if r:
                start_time = r.group(1).replace(':', '')
        if room_id and not hoster and round_number and start_time:
            hoster = '-'
        #房号，房主，局数，开始时间识别结束
        if not caption_start and room_id and hoster and round_number and start_time:
            caption_start = True
            continue
        if caption_start:
            if not caption_user and words['words'].strip() == '玩家':
                player_pos = words['chars'][0]['location']['left']
                pos_range['player']['start'] = player_pos + 20
                pos_range['player']['end'] = pos_range['player']['start'] + 100
                caption_user = True
            if not caption_id and words['words'].strip() == 'ID':
                pos_range['player_id']['start'] = words['chars'][0]['location']['left'] - 10
                pos_range['player_id']['end'] = pos_range['player_id']['start'] + 100
                caption_id = True
            if not caption_score and re.search(r'(.*)积分$', words['words']):
                score_pos = len(words['chars']) - 2
                pos_range['score']['start'] = words['chars'][score_pos]['location']['left'] - 10
                print("score_pos*****************"+str(pos_range['score']['start']))

                pos_range['score']['end'] = pos_range['score']['start'] + 100
                caption_score = True
            #标题部分
            if not player_start and caption_user and caption_id and caption_score:
                player_start = True
                continue
            #标题部分
            if not player_start and caption_user and not caption_id and caption_score:
                rate = player_pos / pos_range['player']['base'] 
                pos_range['player_id']['start'] = pos_range['player_id']['base'] * rate
                pos_range['player_id']['end'] = pos_range['player_id']['start'] + 100
                player_start = True
                continue
            print('player:'+str(player)+'=======player_id:'+str(player_id)+'=======score:'+str(score))
            if player_start:
                if player and player_id and not score:

                    tmp_player_id = ''
                    tmp_score = ''
                    print(player_id_chars)
                    for char in player_id_chars:
                        if char['location']['left'] >= pos_range['player_id']['start'] \
                            and char['location']['left'] < pos_range['score']['start']:
                            tmp_player_id += char['char']
                        else:
                            tmp_score += char['char']

                    player_id = tmp_player_id
                    score = tmp_score
                if not player and player_id and score:
                    player = '-'
                if player and player_id and score:
                    print('玩家:=============='+player)
                    print('玩家Id:==============='+player_id)                
                    print('积分:==============='+score)
                    data_list.append({
                        'name':player,
                        'id':int(player_id),
                        'score':int(score)
                    })
                    if player == hoster:
                        hoster_id = player_id
                    player = None
                    player_id = None
                    score = None
                is_player_id = re.search(r'^\d+', words['words']) or re.search(r'^\d+-\d+', words['words'])
                is_score =  re.search(r'^\d+', words['words']) or re.search(r'^-\d+', words['words'])
                if words['chars'][0]['location']['left'] >= pos_range['player']['start'] \
                    and words['chars'][0]['location']['left'] < pos_range['player_id']['start']:
                    player = words['words']
                    player_chars = words['chars']
                elif is_player_id and words['chars'][0]['location']['left'] >= pos_range['player_id']['start'] \
                    and words['chars'][0]['location']['left'] < pos_range['score']['start']:
                    player_id = words['words']
                    player_id_chars = words['chars']
                    if not player:
                        player = '-'
                elif is_score and words['chars'][0]['location']['left'] >= pos_range['score']['start'] \
                    and words['chars'][0]['location']['left'] < pos_range['score']['end']:
                    score = words['words']
                    score_chars = words['chars']

    room_data = playerResult.roomData()
    room_data.roomId = room_id
    room_data.startTime = start_time
    room_data.roomHosterId = hoster_id
    room_data.roomHoster = hoster
    room_data.roundCounter = round_number
    total = 0
    for player in data_list:
        p = playerResult.playerData()
        p.name = player['name']
        p.id = player['id']
        p.score = player['score']
        total += abs(p.score)
        room_data.playerData.append(p)

    # 如果能识别正负，加下面的部分有什么用？如果不能，用abs做什么？偶尔能识别？，下面第一条，不管怎么样，都是正数吧，除非是排序上正数总体在前
    # 默认似乎是降序排列的，但最好是能完美识别，不然太依赖顺序了
    score = 0
    for playerData in room_data.playerData:
        if score + abs(playerData.score) > total / 2:
            playerData.score = -abs(playerData.score)
        else:
            playerData.score = abs(playerData.score)
        score += abs(playerData.score)
    return room_data

#itchat 实例列表
_list = {}

class wechatInstance():

    def scanError(self, room_data, total_score, fileName):
        erro_msg = ""
        if room_data.startTime == '' or room_data.roomId == 0 or total_score != 0 \
                or room_data.roundCounter == 0 or len(room_data.playerData) == 0:
            erro_msg = '图片无法识别\n'
            erro_msg += 'roomId:' + str(room_data.roomId) + '\n'
            erro_msg += 'startTime:' + str(room_data.startTime) + '\n'
            erro_msg += 'roomHosterId:' + str(room_data.roomHosterId) + '\n'
            erro_msg += 'roomHoster:' + str(room_data.roomHoster) + '\n'
            erro_msg += 'roundCounter:' + str(room_data.roundCounter) + '\n'
            erro_msg += 'players:' + str(len(room_data.playerData)) + '\n'
            erro_msg += 'total_score:' + str(total_score)

            wrong_image = WrongImage(club_name=self.club.user_name, image=fileName, create_time=int(time.time()))
            wrong_image.save()
            self.itchat_instance.send(erro_msg, 'filehelper')
        return erro_msg

    def createTempPlayer(self, room_data, num):
        self.itchat_instance.send(
            '用户id：' + str(room_data.playerData[num].id) + '没有注册, 创建临时账号：' + room_data.playerData[num].name,
            'filehelper')
        player = Player(wechat_nick_name=room_data.playerData[num].name, nick_name=room_data.playerData[num].name,
                        club=self.club, current_score=0, history_profit=0)
        player.save()
        gameid = GameID(club=self.club, player=player, gameid=room_data.playerData[num].id,
                        game_nick_name=room_data.playerData[num].name)
        gameid.save()

    def __init__(self, uuid):
        self.qrid = itchat.get_QRuuid()
        self.logined = False
        self.itchat_instance = itchat.new_instance()
        try:
            self.club = Clubs.objects.get(user_name=uuid)
        except:
            print("club未找到：" % uuid)

        # # 接受文字命令的 逻辑处理
        # #@self.itchat_instance.msg_register(itchat.content.TEXT)
        # def simple_reply(msg):
        #     self.club = Clubs.objects.get(user_name=self.club.user_name)
        #     if self.club.expired_time < time.time():
        #         self.itchat_instance.send('CD KEY 已失效。 请延长后继续使用。', 'filehelper')
        #         self.itchat_instance.logout()
        #         return
        #     if msg['ToUserName'] == 'filehelper':
        #         if msg['Type'] == 'Text':
        #             contentSplit = msg['Content'].split('**')
        #
        #             #注册用户
        #             if contentSplit[0] == '注册':
        #                  if len(contentSplit) != 2:
        #                      self.itchat_instance.send('参数错误', 'filehelper')
        #                      return '命令执行失败: %s' % msg['Content']
        #
        #                  try:
        #                      player = Player.objects.get(wechat_nick_name=contentSplit[1])
        #                      self.itchat_instance.send('用户:' + contentSplit[1] + ' 已经存在。', 'filehelper')
        #                      return '命令执行失败: %s' % msg['Content']
        #                  except Player.DoesNotExist:
        #                      player = Player(wechat_nick_name=contentSplit[1], club=self.club, current_score=0, history_profit=0)
        #                      player.save()
        #                      self.itchat_instance.send('注册用户:' + player.wechat_nick_name, 'filehelper')
        #                      return '命令执行完成: %s' % msg['Content']
        #
        #             #绑定游戏id
        #             elif contentSplit[0] == '绑定游戏id':
        #                  if  len(contentSplit) != 4:
        #                      self.itchat_instance.send('参数错误', 'filehelper')
        #                      return '命令执行失败: %s' % msg['Content']
        #
        #                  player = None
        #                  try:
        #                      player = Player.objects.get(wechat_nick_name=contentSplit[1], club=self.club)
        #                  except Player.DoesNotExist:
        #                      self.itchat_instance.send('用户:' + contentSplit[1] + '不存在，请先注册用户', 'filehelper')
        #                      return '命令执行失败: %s' % msg['Content']
        #
        #                  try:
        #                      gameID = GameID.objects.get(gameid=contentSplit[2])
        #                      if gameID.player.wechat_nick_name == 'tempUser':
        #                          gameID.player.wechat_nick_name = contentSplit[1]
        #                          gameID.player.save()
        #                          self.itchat_instance.send('游戏id绑定成功', 'filehelper')
        #                          return '命令执行成功: %s' % msg['Content']
        #                      else :
        #                          self.itchat_instance.send('游戏id已绑定', 'filehelper')
        #                          return '命令执行失败: %s' % msg['Content']
        #                  except GameID.DoesNotExist:
        #                      player = Player.objects.get(wechat_nick_name=contentSplit[1], club=self.club)
        #                      gameID = GameID(player=player, gameid=contentSplit[2], game_nick_name=contentSplit[3])
        #                      gameID.save()
        #                      self.itchat_instance.send('游戏id绑定成功', 'filehelper')
        #                      return '命令执行成功: %s' % msg['Content']
        #
        #             #上分
        #             elif contentSplit[0] == '上分':
        #                  if  len(contentSplit) != 3:
        #                      self.itchat_instance.send('参数错误', 'filehelper')
        #                      return '命令执行失败: %s' % msg['Content']
        #
        #                  try:
        #                      player = Player.objects.get(wechat_nick_name=contentSplit[1], club=self.club)
        #                      player.current_score = player.current_score + int(contentSplit[2])
        #                      player.save()
        #                  except Player.DoesNotExist:
        #                      self.itchat_instance.send('用户:' + contentSplit[1] + '不存在，请先注册用户', 'filehelper')
        #                      return '命令执行失败: %s' % msg['Content']
        #                  except TypeError:
        #                      self.itchat_instance.send('类型错误，请检查上分参数', 'filehelper')
        #                      return '命令执行失败: %s' % msg['Content']
        #
        #
        #                      self.itchat_instance.send('用户:' + contentSplit[1] + '上分成功, 上分数量' + str(contentSplit[2]), 'filehelper')
        #                      return '命令执行成功: %s' % msg['Content']
        #                  self.itchat_instance.send('上分:' + contentSplit[1], 'filehelper')
        #                  return '命令执行成功: %s' % msg['Content']
        #             #下分
        #             elif contentSplit[0] == '下分':
        #                  if  len(contentSplit) != 3:
        #                      self.itchat_instance.send('参数错误', 'filehelper')
        #                      return '命令执行失败: %s' % msg['Content']
        #                  current_score = 0
        #                  try:
        #                      player = Player.objects.get(wechat_nick_name=contentSplit[1], club=self.club)
        #                      downNumber = int(contentSplit[2])
        #                      if player.current_score < downNumber:
        #                          self.itchat_instance.send('用户分数不足,当前分数：' + str(player.current_score), 'filehelper')
        #                          return '命令执行失败: %s' % msg['Content']
        #                      else :
        #                          current_score = player.current_score = player.current_score - downNumber
        #                          player.save()
        #                  except Player.DoesNotExist:
        #                      self.itchat_instance.send('用户:' + contentSplit[1] + '不存在，请先注册用户', 'filehelper')
        #                      return '命令执行失败: %s' % msg['Content']
        #                  except TypeError:
        #                      self.itchat_instance.send('类型错误，请检查上分参数', 'filehelper')
        #                      return '命令执行失败: %s' % msg['Content']
        #
        #                  self.itchat_instance.send('用户:' + contentSplit[1] + '下分成功, 下分数量' + str(contentSplit[2])\
        #                  + '当前分数：' + str(current_score) , 'filehelper')
        #                  return '命令执行成功: %s' % msg['Content']
        #
        #
        #             #查看单个用户战绩
        #             elif contentSplit[0] == '查看单个用户战绩':
        #                  if  len(contentSplit) != 2:
        #                      self.itchat_instance.send('参数错误', 'filehelper')
        #                      return '命令执行失败: %s' % msg['Content']
        #
        #                  getPlayerScore(contentSplit[1], self.itchat_instance, self)
        #
        #                  return '命令执行成功: %s' % msg['Content']
        #
        #             #查看所有用户战绩
        #             elif contentSplit[0] == '查看所有用户战绩':
        #                  players = Player.objects.filter(club=self.club)
        #                  result = '';
        #                  for player in players:
        #                     result += player.wechat_nick_name + '当前分数：' + str(player.current_score) + '\n' + \
        #                                     player.wechat_nick_name + '历史战绩：' + str(player.history_profit) + '\n\n';
        #                  self.itchat_instance.send(result, 'filehelper')
        #                  return '命令执行成功: %s' % msg['Content']
        #
        #             #设置管理费模式
        #             elif contentSplit[0] == '设置手续费模式':#0：固定分数段模式，1：百分比模式，
        #                  if  len(contentSplit) != 3:
        #                      self.itchat_instance.send('参数错误', 'filehelper')
        #                      return '命令执行失败: %s' % msg['Content']
        #                  try:
        #                      self.club.cost_mode = int(contentSplit[1])
        #                      self.club.cost_param = contentSplit[2]
        #                      self.club.save()
        #                  except TypeError:
        #                      self.itchat_instance.send('类型错误，请检查参数', 'filehelper')
        #                      return '命令执行失败: %s' % msg['Content']
        #
        #                  self.itchat_instance.send('设置手续费模式:' + contentSplit[1], 'filehelper')
        #                  return '命令执行成功: %s' % msg['Content']
        #
        #
        #             #查看盈利
        #             elif contentSplit[0] == '查看整体盈利':
        #                  self.itchat_instance.send('查看整体盈利:' + str(self.club.profit), 'filehelper')
        #                  return '命令执行成功: %s' % msg['Content']
        #
        #             #用户改名
        #             elif contentSplit[0] == '用户改名':
        #                  if  len(contentSplit) != 3:
        #                      self.itchat_instance.send('参数错误', 'filehelper')
        #                      return '命令执行失败: %s' % msg['Content']
        #
        #                  try:
        #                      player = Player.objects.get(wechat_nick_name=contentSplit[1], club=self.club)
        #                      player.wechat_nick_name = contentSplit[2]
        #                      player.save()
        #                      self.itchat_instance.send('用户改名:' + contentSplit[1], 'filehelper')
        #                      return '命令执行成功: %s' % msg['Content']
        #                  except Player.DoesNotExist:
        #                      self.itchat_instance.send('用户:' + contentSplit[1] + '不存在，请先注册用户', 'filehelper')
        #                      return '命令执行失败: %s' % msg['Content']
        #
        #                  self.itchat_instance.send('用户改名:' + contentSplit[1], 'filehelper')
        #                  return '命令执行成功: %s' % msg['Content']
        #
        #             #新增介绍人
        #             elif contentSplit[0] == '新增介绍人':
        #                  if  len(contentSplit) != 3:
        #                      self.itchat_instance.send('参数错误', 'filehelper')
        #                      return '命令执行失败: %s' % msg['Content']
        #                  try:
        #                      player = Player.objects.get(wechat_nick_name=contentSplit[1], club=self.club)
        #                      player.introducer = contentSplit[2]
        #                      player.save()
        #                      self.itchat_instance.send('设置介绍人成功！' + player.wechat_nick_name + ' 现在的介绍人是：' + player.introducer , 'filehelper')
        #                      return '命令执行成功: %s' % msg['Content']
        #                  except Player.DoesNotExist:
        #                      self.itchat_instance.send('用户:' + contentSplit[1] + '不存在，请先注册用户', 'filehelper')
        #                      return '命令执行失败: %s' % msg['Content']
        #
        #             #查看介绍人
        #             elif contentSplit[0] == '查看介绍人':
        #                  if  len(contentSplit) != 2:
        #                      self.itchat_instance.send('参数错误', 'filehelper')
        #                      return '命令执行失败: %s' % msg['Content']
        #
        #                  try:
        #                      player = Player.objects.get(wechat_nick_name=contentSplit[1], club=self.club)
        #                      self.itchat_instance.send(player.wechat_nick_name + '现在的介绍人是：' + player.introducer , 'filehelper')
        #                      return '命令执行成功: %s' % msg['Content']
        #                  except Player.DoesNotExist:
        #                      self.itchat_instance.send('用户:' + contentSplit[1] + '不存在，请先注册用户', 'filehelper')
        #                      return '命令执行失败: %s' % msg['Content']
        #
        #             #查看房主
        #             elif contentSplit[0] == '查看房主':
        #                  players = Player.objects.filter(club=self.club)
        #                  for player in players:
        #                      if player.today_hoster_number > 0:
        #                         getPlayerScore(player[num].wechat_nick_name + '今日房主数量：' + str(player[num].today_hoster_number) , self.itchat_instance)
        #
        #             #注销
        #             elif contentSplit[0] == '注销':
        #                 self.itchat_instance.send('再见！', 'filehelper')
        #                 self.itchat_instance.logout()
        #
        #             #查看用户战绩
        #             elif contentSplit[0] == '查看游戏用户战绩':
        #                 if len(contentSplit) != 2:
        #                     self.itchat_instance.send('参数错误', 'filehelper')
        #                     return '命令执行失败: %s' % msg['Content']
        #                 cursor=connection.cursor()
        #                 sql = " select player.* from DServerAPP_player player , DServerAPP_gameid gameid"
        #                 sql+= " where player.id=gameid.player_id and gameid='"+contentSplit[1]+"'"
        #                 cursor.execute(sql)
        #                 players = cursor.fetchall()
        #                 result = '';
        #                 for player in players:
        #                    result += player[2] + '当前分数：' + str(player[4]) + '\n' + \
        #                                    player[2] + '历史战绩：' + str(player[5]) + '\n\n';
        #                 self.itchat_instance.send(result, 'filehelper')
        #                 return '命令执行成功: %s' % msg['Content']
        #             #错误图片
        #             elif contentSplit[0] == '错误图片':
        #                 date = None
        #                 club_path = settings.STATIC_ROOT + '/upload/' + self.club.user_name + '/'
        #
        #                 if len(contentSplit) == 2:
        #                     date = contentSplit[1]
        #                 else:
        #                     date = datetime.datetime.now().strftime('%Y-%m-%d')
        #                 cursor=connection.cursor()
        #                 sql = " select image from DServerAPP_wrongimage"
        #                 sql+= " where club_name='" +self.club.user_name+ "' and from_unixtime(create_time,'%Y-%m-%d')='"+date+"'"
        #                 cursor.execute(sql)
        #                 objs = cursor.fetchall()
        #
        #                 for obj in objs:
        #                     img_file = club_path + obj[0]
        #                     self.itchat_instance.send_image(img_file, 'filehelper')
        #                 if len(objs) == 0:
        #                     self.itchat_instance.send("无错误图片", 'filehelper')
        #             elif contentSplit[0] == '好友':
        #                 #print(self.itchat_instance.get_friends(update=True))
        #                 f = self.itchat_instance.search_friends(remarkName='夜魔1')
        #                 print(f)
        #                 print(type(f))
        #                 '''
        #                 f = self.itchat_instance.search_friends(remarkName='创世纪')
        #                 if f:
        #                     print(f[0]['UserName'])
        #                     print(self.itchat_instance.set_alias(f[0]['UserName'], '夜魔1'))
        #                     f = self.itchat_instance.search_friends(remarkName='夜魔1')
        #                     print(f[0]['UserName'])
        #                 '''
        #             elif len(contentSplit) == 1:
        #                 try :
        #                     theID = int(contentSplit[0])
        #                     gameID = GameID(gameid=theID)
        #                     self.itchat_instance.send('用户当前分数：' + str(gameID.player.current_score) + \
        #                     '用户历史战绩：' + str(gameID.player.history_profit), 'filehelper')
        #                 except GameID.DoesNotExist:
        #                     self.itchat_instance.send('用户' + str(theID) + '不存在', 'filehelper')
        #                 except:
        #                     self.itchat_instance.send('发生异常', 'filehelper')
        #
        #             return '命令执行完成: %s' % msg['Content']


        # 接受图片的逻辑处理
        @self.itchat_instance.msg_register([PICTURE])
        def download_files_new(msg):
            # 失效判断，应该在登录的一瞬间自动判断，然后失效则发送消息后，自动注销
            if self.club.expired_time < time.time():
                self.itchat_instance.send('CD KEY 已失效。 请延长后继续使用。', 'filehelper')
                self.itchat_instance.logout()
                return

            if msg['ToUserName'] != 'filehelper':
                return

            self.itchat_instance.send('正在识别...', 'filehelper')

            club_path = settings.STATIC_ROOT + '/upload/' + self.club.user_name + '/'
            if not os.path.exists(club_path):
                os.mkdir(club_path)
            img_file = club_path + msg.fileName
            msg.download(img_file)
            typeSymbol = {
                PICTURE: 'img',
                }.get(msg.type, 'fil')

            # 网络图片文字文字识别接口
            result = aipOcr.accurate(get_file_content(img_file),options)

            #从识别的文本中抓取最终结果
            resultDir = result['direction']#0:是正常方向，3是顺时针90度
            wordsArray = result['words_result']
            room_data = get_pic_info(wordsArray)
            total_score = 0
            for playerData in room_data.playerData:
                total_score += playerData.score

            if self.scanError(room_data, total_score, msg.fileName):
                # 图片无法识别
                return
            #根据刷新时间设置，设置入库时间
            today_time_start = '%s-%s-%s 0:0:0' % (timezone.now().year, timezone.now().month, timezone.now().day)
            timeArray = time.strptime(today_time_start, "%Y-%m-%d %H:%M:%S")
            today_time_start = int(time.mktime(timeArray))

            # 这个刷新时间有什么用？
            refresh_time = timezone.now()
            if time.time() < today_time_start + self.club.refresh_time * 3600:
                refresh_time = timezone.now() - datetime.timedelta(days=1)
            try:
                HistoryGame.objects.get(club_id=self.club.uuid, room_id=room_data.roomId, start_time=room_data.startTime)
                self.itchat_instance.send('数据已入库！', 'filehelper')      
                return ''
            except HistoryGame.DoesNotExist:
                playerData = []
                for d in room_data.playerData:
                    playerData.append(d.dumps())
                historyGame = HistoryGame(club=self.club, room_id=room_data.roomId, hoster_name=room_data.roomHoster,\
                hoster_id=room_data.roomHosterId, round_number=room_data.roundCounter, start_time=room_data.startTime, \
                player_data=json.dumps(playerData), create_time=timezone.now(), refresh_time=refresh_time)
                historyGame.save()
                room_data.toString()
                pic_msg = '房间ID：' + str(room_data.roomId) + '\n'
                pic_msg+= '房主：' + str(room_data.roomHoster) + '\n'
                pic_msg+= '房主ID：' + str(room_data.roomHosterId) + '\n'
                pic_msg+= '局数：' + str(room_data.roundCounter) + '\n'
                pic_msg+= '开始时间：' + str(room_data.startTime) + '\n'
                pic_msg+= '-------------------------------------\n'

                #管理员
                manager_wechat_uuids = []
                for manager in Manager.objects.filter(club=self.club):
                    f = self.itchat_instance.search_friends(remarkName=manager.nick_name)
                    if f:
                        if isinstance(f,list):
                            manager_wechat_uuids.append(f[0]['UserName'])
                        elif isinstance(f,dict):
                            manager_wechat_uuids.append(f['UserName'])

                rules = []
                if self.club.cost_param == None or self.club.cost_param == 'none' or self.club.cost_param == '':
                    pass
                else:
                    rules = self.club.cost_param
                    rules = rules.split('|')
                costMode = self.club.cost_mode

                clubProfit = 0
                
                for num in range(0, len(room_data.playerData)):
                    roomPlayData = room_data.playerData[num]
                    player = None
                    wechat_uuid = None
                    has_gameid = False
                    cost = 0

                    is_host = 1 if roomPlayData.name == room_data.roomHoster else 0

                    # 获取当前用户的username用来发送消息
                    try:
                        matchGi = GameID.objects.get(club=self.club, gameid=roomPlayData.id, player__is_del=0)
                    except GameID.DoesNotExist:
                        pass
                    else:
                        has_gameid = True
                        toPlayer = self.getWechatUserByRemarkName(matchGi.player.nick_name)
                        if toPlayer:
                            wechat_uuid = toPlayer['UserName']

                    # 数据库中没有用户，自动增加
                    if not has_gameid:
                        self.createTempPlayer(room_data, num)

                    if is_host:
                        player.today_hoster_number += 1
                    try:
                        last_current_score = player.current_score;

                        if len(rules) > 0:
                            if costMode == 0 and num < int(rules[0]):
                                value = int(rules[2])
                                params = rules[1].split('_')
                                if params[num].isdigit():
                                    cost = int(params[num])
                                else:
                                    cost = int(roomPlayData.score * float(params[num]))

                                if roomPlayData.score > value:
                                    costed = True
                            elif costMode == 1 and num < int(rules[0]):
                                ranges = rules[1].split('*')
                                costs = rules[2].split('*')
                                cost = 0
                                for index, range_ in enumerate(ranges):
                                    if num == index:
                                        costs_ = costs[index].split('_')
                                        for rindex, rrange_ in enumerate(range_.split('_')):
                                            if roomPlayData.score < int(rrange_):
                                                cost = int(costs_[rindex])
                                                break
                                if cost > 0:
                                    costed = True
                            elif costMode == 2:
                                values = rules[0].split('_')
                                costs = rules[1].split('_')
                                can_cost = False
                                for index, value in enumerate(values):
                                    if roomPlayData.score >= int(value):
                                        can_cost = True
                                        break
                                #所有固定模式
                                if can_cost:
                                    cost = int(costs[index])
                                    costed = True


                        # 整合三个mode下的代码，原型
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

                        costShow1 = "  管理费: %s" % cost
                        costShow2 = "  本局房费: %s" % cost
                        if cost == 0:
                            costShow1 = ""
                            costShow2 = "  本局房费: 无"

                        pic_msg += str(num + 1) + '.ID' + str(roomPlayData.id) + '：' + player.nick_name + '  分数：' + str(roomPlayData.score) + \
                                   costShow1 + '  总分数：' + str(player.current_score) + '\n'
                        if wechat_uuid:
                            self.itchat_instance.send_image(img_file, wechat_uuid)
                            alert_msg = player.nick_name + '\n'
                            alert_msg += '上次积分: ' + str(last_current_score) + '\n'
                            alert_msg += '本局积分: ' + str(roomPlayData.score) + '\n'
                            alert_msg += costShow2 + '\n'
                            alert_msg += '当前余分: ' + str(player.current_score) + '\n'
                            self.itchat_instance.send(alert_msg, wechat_uuid)

                        #授信
                        if player.score_limit !=0 and player.current_score <= -player.score_limit:
                            alert_msg = player.nick_name + '\n'
                            alert_msg+= '上分提醒\n'
                            alert_msg+= '当前余分: '+str(player.current_score) + '\n'
                            alert_msg+= player.score_limit_desc + '\n'
                            alert_msg+= '本条消息来自傻瓜机器人自动回复\n'
                            if wechat_uuid:
                                self.itchat_instance.send(alert_msg, wechat_uuid)
                            for manager_wechat_uuid in manager_wechat_uuids:
                                self.itchat_instance.send(alert_msg, manager_wechat_uuid)

                    except:
                        traceback.print_exc()
                        self.itchat_instance.send('发生异常！', 'filehelper')
                        continue
                historyGame.save()        
          
            self.club.profit += clubProfit
            self.club.save()
            pic_msg+= '-------------------------------------\n'
            pic_msg+= '获得管理费：' + str(clubProfit)
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

    def is_login(self):
        if self.itchat_instance.alive:
            return True
        else:
            return False

    def get_uuid(self):
        return self.itchat_instance.get_QRuuid()

    def check_login(self, uuid):
        self.checked = False
        def _check():
            while  not self.checked:
                status = self.itchat_instance.check_login(uuid)
                print('check login.'+status)

                if status == '200':
                    userInfo = self.itchat_instance.web_init()
                    self.itchat_instance.show_mobile_login()
                    self.itchat_instance.get_contact(update=True)
                    output_info('Login successfully as %s'%userInfo['User']['NickName'])
                    self.itchat_instance.start_receiving()
                    self.itchat_instance.run(blockThread=False)
                    print('start itchat....')
                    self.checked = True
                elif status == '201':
                    pass
                else:
                    self.checked = True
                time.sleep(1)
        t = threading.Thread(target=_check)
        t.setDaemon(True)
        t.start()

    def logout(self):
        self.itchat_instance.logout()

    def run(self):
        print('thread start')
        self.itchat_instance.run()

    def send(self, user_name, msg):
        r = self.itchat_instance.send(msg, user_name)
        print(msg)
        print(user_name)
        print(r)


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


