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

def getRoomIDAndHoster(rowData, index):
    print('walawala===='+rowData[index].words)
    roomId = 0
    hoster = ''
    flag1 = rowData[index].words.find(':')
    rawId = rowData[index].words[flag1 + 1:].strip().replace(' ','')

    if rawId.isdigit():
        roomId = int(rawId)
    else:
        numberList = []
        for char in rawId:
            if char.isdigit():
                numberList.append(int(char))
                print(char)
            else:
                print('fuck:' + char)
        
        length = len(numberList)
        roomId = 0
        for num in range(0, len(numberList)):
            roomId += numberList[num] * pow(10, length - num - 1)
    print('the roomId is:' + str(roomId))
    flag2 = rowData[index + 1].words.find(':')
    hoster = rowData[index + 1].words[flag2 + 1:]
    return roomId, hoster

def getRoundNumberAndStartTime(rowData):
    roundNumber = 0
    idLeftPos = 0
    startTime = ''
    flag1 = rowData[0].words.find(':')
    print('the round number string is:' + rowData[0].words[flag1 + 1:])
    roundNumber = int(rowData[0].words[flag1 + 1:])
    print('the new round nubmer is:' + str(roundNumber))
    flag2 = rowData[1].words.find(':')
    startTime = rowData[1].words[flag2 + 1:]
    if '开' in rowData[1].words:
        index = rowData[1].words.find('开')
        idLeftPos = int(rowData[1].chars[index]['location']['left']) + int(rowData[1].chars[index]['location']['width']) + 13
    if '始' in rowData[1].words:
        index = rowData[1].words.find('始')
        idLeftPos = int(rowData[1].chars[index]['location']['left'])
    if '时' in rowData[1].words:
        index = rowData[1].words.find('时')
        idLeftPos = int(rowData[1].chars[index]['location']['left']) - int(rowData[1].chars[index]['location']['width']) - 26
    if '间' in rowData[1].words:
        index = rowData[1].words.find('间')
        idLeftPos = int(rowData[1].chars[index]['location']['left']) - int(rowData[1].chars[index]['location']['width']) * 2 - 26
    return roundNumber, startTime, idLeftPos

def updatePlayerScore(gameid, score):
    try:
        gameID = GameID.objects.get(gameid=gameid)
        return 0
    except GameID.DoesNotExist:
        return -1

def getPlayerScore(nickName, itchatInstance, self):
    try:
        player = Player.objects.get(wechat_nick_name=nickName, club=self.club)
        itchatInstance.send('用户当前分数：' + str(player.current_score) + \
        '用户历史战绩：' + str(player.history_profit), 'filehelper')
    except Player.DoesNotExist:
        itchatInstance.send('用户:' + nickName + '不存在，请先注册用户', 'filehelper')
        return '命令执行失败: %s' % msg['Content']

def get_data_pos(index, result):
    pos = {}
    pos = []
    for i, words in enumerate(result):
        if i <= index:
            continue
        left = words['chars'][0]['location']['left']
        pos.append(left)
    pos.sort()
    print(pos)

def get_pic_info(result):
    # print(result)
    # return
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

    score = 0
    for playerData in room_data.playerData:
        if score + abs(playerData.score) > total / 2:
            playerData.score = -abs(playerData.score)
        else:
            playerData.score = abs(playerData.score)
        score += abs(playerData.score)
    print(room_data)
    return room_data

def get_template_pic_info(result):
    room_id = 0
    hoster = None
    hoster_id = 0
    round_number = 0
    start_time = None

    data_list = []
    for index, words in enumerate(result):
        if not room_id and words["word_name"] == "room_id":
            room_id = words["word"]
        elif not hoster and words["word_name"] == "hoster_name":
            hoster = words["word"]
        elif not round_number and words["word_name"] == "round_number":
            round_number = words["word"]
        elif not start_time and words["word_name"] == "start_date":
            start_time = words["word"]
        if room_id and not hoster and round_number and start_time:
            hoster = '-'

        r = re.match(r'player_info#(\d+)#(.*)', words["word_name"], re.M | re.I)
        if r:
            player_index = int(r.group(1))
            player_attr = r.group(2)
            while(len(data_list) < player_index):
                data_list.append({})
            data_list[player_index-1][player_attr] = words["word"]

    room_data = playerResult.roomData()
    room_data.roomId = room_id
    room_data.startTime = start_time
    room_data.roomHoster = hoster
    room_data.roundCounter = round_number
    total = 0
    for player in data_list:
        print("内容:\n%s" % player)
        p = playerResult.playerData()
        p.name = player['name']
        p.id = int(player['id'])
        p.score = int(player['score'])
        total += abs(p.score)
        room_data.playerData.append(p)
        if p.name == hoster:
            hoster_id = p.id

    room_data.roomHosterId = hoster_id
    score = 0
    for playerData in room_data.playerData:
        if score + abs(playerData.score) > total / 2:
            playerData.score = -abs(playerData.score)
        else:
            playerData.score = abs(playerData.score)
        score += abs(playerData.score)
    print(room_data)
    return room_data

#itchat 实例列表
_list = {}

class wechatInstance():

    def __init__(self,uuid):
        clubInstance = None
        self.qrid = itchat.get_QRuuid()
        self.logined = False
        clubInstance = Clubs.objects.get(user_name=uuid)
        self.itchat_instance = itchat.new_instance()
        self.club = clubInstance

        # 接受文字命令的 逻辑处理
        #@self.itchat_instance.msg_register(itchat.content.TEXT)
        def simple_reply(msg):
            clubInstance = Clubs.objects.get(user_name=self.club.user_name)
            if clubInstance.expired_time < time.time():
                self.itchat_instance.send('CD KEY 已失效。 请延长后继续使用。', 'filehelper')
                self.itchat_instance.logout()
                return
            if msg['ToUserName'] == 'filehelper':
                if msg['Type'] == 'Text':
                    contentSplit = msg['Content'].split('**')

                    #注册用户
                    if contentSplit[0] == '注册':
                         if len(contentSplit) != 2:
                             self.itchat_instance.send('参数错误', 'filehelper')   
                             return '命令执行失败: %s' % msg['Content']  

                         try:
                             player = Player.objects.get(wechat_nick_name=contentSplit[1])
                             self.itchat_instance.send('用户:' + contentSplit[1] + ' 已经存在。', 'filehelper')
                             return '命令执行失败: %s' % msg['Content']
                         except Player.DoesNotExist:
                             player = Player(wechat_nick_name=contentSplit[1], club=self.club, current_score=0, history_profit=0)
                             player.save()
                             self.itchat_instance.send('注册用户:' + player.wechat_nick_name, 'filehelper')
                             return '命令执行完成: %s' % msg['Content']

                    #绑定游戏id
                    elif contentSplit[0] == '绑定游戏id':
                         if  len(contentSplit) != 4:
                             self.itchat_instance.send('参数错误', 'filehelper')   
                             return '命令执行失败: %s' % msg['Content']  

                         player = None
                         try:
                             player = Player.objects.get(wechat_nick_name=contentSplit[1], club=self.club)
                         except Player.DoesNotExist:
                             self.itchat_instance.send('用户:' + contentSplit[1] + '不存在，请先注册用户', 'filehelper')
                             return '命令执行失败: %s' % msg['Content']

                         try:
                             gameID = GameID.objects.get(gameid=contentSplit[2])
                             if gameID.player.wechat_nick_name == 'tempUser':
                                 gameID.player.wechat_nick_name = contentSplit[1]
                                 gameID.player.save()
                                 self.itchat_instance.send('游戏id绑定成功', 'filehelper') 
                                 return '命令执行成功: %s' % msg['Content']     
                             else :
                                 self.itchat_instance.send('游戏id已绑定', 'filehelper')   
                                 return '命令执行失败: %s' % msg['Content']  
                         except GameID.DoesNotExist:
                             player = Player.objects.get(wechat_nick_name=contentSplit[1], club=self.club)
                             gameID = GameID(player=player, gameid=contentSplit[2], game_nick_name=contentSplit[3])
                             gameID.save()
                             self.itchat_instance.send('游戏id绑定成功', 'filehelper')   
                             return '命令执行成功: %s' % msg['Content']     

                    #上分
                    elif contentSplit[0] == '上分':
                         if  len(contentSplit) != 3:
                             self.itchat_instance.send('参数错误', 'filehelper')   
                             return '命令执行失败: %s' % msg['Content']  

                         try:
                             player = Player.objects.get(wechat_nick_name=contentSplit[1], club=self.club)
                             player.current_score = player.current_score + int(contentSplit[2])
                             player.save()
                         except Player.DoesNotExist:
                             self.itchat_instance.send('用户:' + contentSplit[1] + '不存在，请先注册用户', 'filehelper')
                             return '命令执行失败: %s' % msg['Content']
                         except TypeError:
                             self.itchat_instance.send('类型错误，请检查上分参数', 'filehelper')
                             return '命令执行失败: %s' % msg['Content']


                             self.itchat_instance.send('用户:' + contentSplit[1] + '上分成功, 上分数量' + str(contentSplit[2]), 'filehelper')   
                             return '命令执行成功: %s' % msg['Content']     
                         self.itchat_instance.send('上分:' + contentSplit[1], 'filehelper')
                         return '命令执行成功: %s' % msg['Content']     
                    #下分
                    elif contentSplit[0] == '下分':
                         if  len(contentSplit) != 3:
                             self.itchat_instance.send('参数错误', 'filehelper')   
                             return '命令执行失败: %s' % msg['Content']  
                         current_score = 0
                         try:
                             player = Player.objects.get(wechat_nick_name=contentSplit[1], club=self.club)
                             downNumber = int(contentSplit[2])
                             if player.current_score < downNumber:
                                 self.itchat_instance.send('用户分数不足,当前分数：' + str(player.current_score), 'filehelper')
                                 return '命令执行失败: %s' % msg['Content']
                             else :
                                 current_score = player.current_score = player.current_score - downNumber
                                 player.save()
                         except Player.DoesNotExist:
                             self.itchat_instance.send('用户:' + contentSplit[1] + '不存在，请先注册用户', 'filehelper')
                             return '命令执行失败: %s' % msg['Content']
                         except TypeError:
                             self.itchat_instance.send('类型错误，请检查上分参数', 'filehelper')
                             return '命令执行失败: %s' % msg['Content']

                         self.itchat_instance.send('用户:' + contentSplit[1] + '下分成功, 下分数量' + str(contentSplit[2])\
                         + '当前分数：' + str(current_score) , 'filehelper')   
                         return '命令执行成功: %s' % msg['Content']  


                    #查看单个用户战绩
                    elif contentSplit[0] == '查看单个用户战绩':
                         if  len(contentSplit) != 2:
                             self.itchat_instance.send('参数错误', 'filehelper')   
                             return '命令执行失败: %s' % msg['Content']  
                         
                         getPlayerScore(contentSplit[1], self.itchat_instance, self)
                         
                         return '命令执行成功: %s' % msg['Content']  

                    #查看所有用户战绩
                    elif contentSplit[0] == '查看所有用户战绩':
                         players = Player.objects.filter(club=self.club)
                         result = '';
                         for player in players:
                            result += player.wechat_nick_name + '当前分数：' + str(player.current_score) + '\n' + \
                                            player.wechat_nick_name + '历史战绩：' + str(player.history_profit) + '\n\n';
                         self.itchat_instance.send(result, 'filehelper')
                         return '命令执行成功: %s' % msg['Content']  

                    #设置管理费模式
                    elif contentSplit[0] == '设置手续费模式':#0：固定分数段模式，1：百分比模式， 
                         if  len(contentSplit) != 3:
                             self.itchat_instance.send('参数错误', 'filehelper')   
                             return '命令执行失败: %s' % msg['Content']  
                         try:
                             self.club.cost_mode = int(contentSplit[1])
                             self.club.cost_param = contentSplit[2]
                             self.club.save()
                         except TypeError:
                             self.itchat_instance.send('类型错误，请检查参数', 'filehelper')
                             return '命令执行失败: %s' % msg['Content']

                         self.itchat_instance.send('设置手续费模式:' + contentSplit[1], 'filehelper')
                         return '命令执行成功: %s' % msg['Content']  
                    
                    
                    #查看盈利
                    elif contentSplit[0] == '查看整体盈利':
                         self.itchat_instance.send('查看整体盈利:' + str(self.club.profit), 'filehelper')
                         return '命令执行成功: %s' % msg['Content']  
                    
                    #用户改名
                    elif contentSplit[0] == '用户改名':
                         if  len(contentSplit) != 3:
                             self.itchat_instance.send('参数错误', 'filehelper')   
                             return '命令执行失败: %s' % msg['Content']  

                         try:
                             player = Player.objects.get(wechat_nick_name=contentSplit[1], club=self.club)
                             player.wechat_nick_name = contentSplit[2]
                             player.save()
                             self.itchat_instance.send('用户改名:' + contentSplit[1], 'filehelper')
                             return '命令执行成功: %s' % msg['Content']  
                         except Player.DoesNotExist:
                             self.itchat_instance.send('用户:' + contentSplit[1] + '不存在，请先注册用户', 'filehelper')
                             return '命令执行失败: %s' % msg['Content']

                         self.itchat_instance.send('用户改名:' + contentSplit[1], 'filehelper')
                         return '命令执行成功: %s' % msg['Content']  
                    
                    #新增介绍人
                    elif contentSplit[0] == '新增介绍人':
                         if  len(contentSplit) != 3:
                             self.itchat_instance.send('参数错误', 'filehelper')   
                             return '命令执行失败: %s' % msg['Content']  
                         try:
                             player = Player.objects.get(wechat_nick_name=contentSplit[1], club=self.club)
                             player.introducer = contentSplit[2]
                             player.save()
                             self.itchat_instance.send('设置介绍人成功！' + player.wechat_nick_name + ' 现在的介绍人是：' + player.introducer , 'filehelper')
                             return '命令执行成功: %s' % msg['Content']  
                         except Player.DoesNotExist:
                             self.itchat_instance.send('用户:' + contentSplit[1] + '不存在，请先注册用户', 'filehelper')
                             return '命令执行失败: %s' % msg['Content']

                    #查看介绍人
                    elif contentSplit[0] == '查看介绍人':
                         if  len(contentSplit) != 2:
                             self.itchat_instance.send('参数错误', 'filehelper')   
                             return '命令执行失败: %s' % msg['Content']  

                         try:
                             player = Player.objects.get(wechat_nick_name=contentSplit[1], club=self.club)
                             self.itchat_instance.send(player.wechat_nick_name + '现在的介绍人是：' + player.introducer , 'filehelper')
                             return '命令执行成功: %s' % msg['Content']  
                         except Player.DoesNotExist:
                             self.itchat_instance.send('用户:' + contentSplit[1] + '不存在，请先注册用户', 'filehelper')
                             return '命令执行失败: %s' % msg['Content']

                    #查看房主
                    elif contentSplit[0] == '查看房主':
                         players = Player.objects.filter(club=self.club)
                         for player in players:
                             if player.today_hoster_number > 0:
                                getPlayerScore(player[num].wechat_nick_name + '今日房主数量：' + str(player[num].today_hoster_number) , self.itchat_instance)

                    #注销
                    elif contentSplit[0] == '注销':
                        self.itchat_instance.send('再见！', 'filehelper')   
                        self.itchat_instance.logout()
                    
                    #查看用户战绩
                    elif contentSplit[0] == '查看游戏用户战绩':
                        if len(contentSplit) != 2:
                            self.itchat_instance.send('参数错误', 'filehelper')   
                            return '命令执行失败: %s' % msg['Content'] 
                        cursor=connection.cursor()
                        sql = " select player.* from DServerAPP_player player , DServerAPP_gameid gameid"
                        sql+= " where player.id=gameid.player_id and gameid='"+contentSplit[1]+"'"
                        cursor.execute(sql)
                        players = cursor.fetchall()
                        result = '';
                        for player in players:
                           result += player[2] + '当前分数：' + str(player[4]) + '\n' + \
                                           player[2] + '历史战绩：' + str(player[5]) + '\n\n';
                        self.itchat_instance.send(result, 'filehelper')
                        return '命令执行成功: %s' % msg['Content']  
                    #错误图片
                    elif contentSplit[0] == '错误图片':
                        date = None
                        club_path = settings.STATIC_ROOT + '/upload/' + self.club.user_name + '/'

                        if len(contentSplit) == 2:
                            date = contentSplit[1]
                        else:
                            date = datetime.datetime.now().strftime('%Y-%m-%d')
                        cursor=connection.cursor()
                        sql = " select image from DServerAPP_wrongimage"
                        sql+= " where club_name='" +self.club.user_name+ "' and from_unixtime(create_time,'%Y-%m-%d')='"+date+"'"
                        cursor.execute(sql)
                        objs = cursor.fetchall()

                        for obj in objs:
                            img_file = club_path + obj[0]
                            self.itchat_instance.send_image(img_file, 'filehelper')
                        if len(objs) == 0:
                            self.itchat_instance.send("无错误图片", 'filehelper')
                    elif contentSplit[0] == '好友':
                        #print(self.itchat_instance.get_friends(update=True))
                        f = self.itchat_instance.search_friends(remarkName='夜魔1')
                        print(f)
                        print(type(f))
                        '''
                        f = self.itchat_instance.search_friends(remarkName='创世纪')
                        if f:
                            print(f[0]['UserName'])
                            print(self.itchat_instance.set_alias(f[0]['UserName'], '夜魔1'))
                            f = self.itchat_instance.search_friends(remarkName='夜魔1')
                            print(f[0]['UserName'])
                        '''
                    elif len(contentSplit) == 1:
                        try :
                            theID = int(contentSplit[0])
                            gameID = GameID(gameid=theID)
                            self.itchat_instance.send('用户当前分数：' + str(gameID.player.current_score) + \
                            '用户历史战绩：' + str(gameID.player.history_profit), 'filehelper')
                        except GameID.DoesNotExist:
                            self.itchat_instance.send('用户' + str(theID) + '不存在', 'filehelper')
                        except:
                            self.itchat_instance.send('发生异常', 'filehelper')

                    return '命令执行完成: %s' % msg['Content']

        # 接受图片的逻辑处理
        def download_files(msg):
            clubInstance = Clubs.objects.get(user_name=self.club.user_name)
            if clubInstance.expired_time < time.time():
                self.itchat_instance.send('CD KEY 已失效。 请延长后继续使用。', 'filehelper')
                self.itchat_instance.logout()
                return

            if msg['ToUserName'] != 'filehelper':
                return

            self.itchat_instance.send('正在识别...', 'filehelper')

            club_path = settings.STATIC_ROOT + '/upload/' + clubInstance.user_name + '/'
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
            #把数据按坐标排序
            dataTable = {}
            if resultDir == 0:
                for item in wordsArray:
                    print(item['words'])
                    topAnchor = item['chars'][0]['location']['top']
                    if dataTable == None:
                        dataTable[topAnchor] = createQuadList(item)
                    else:
                        rowKey = getCloseAnchor(dataTable, topAnchor,  item['chars'][0]['location']['height'])
                        if rowKey == 0:
                            dataTable[topAnchor] = createQuadList(item)
                        else:
                            quadList = dataTable[rowKey]
                            leftAnchor = item['chars'][0]['location']['left']
                            for num in range(0,len(quadList)):
                                if leftAnchor < quadList[num].leftAnchor:
                                    quadList.insert(num, createCQ(item))
                                    break
                                elif num == len(quadList) - 1:
                                    quadList.append(createCQ(item))

            sortedKeys = sorted(dataTable)

            for key in sortedKeys:
                 quadList = dataTable[key]
                 rowString = ''
                 for num in range(0, len(quadList)):
                     rowString = rowString + quadList[num].words + ', '
                 print(rowString)

            #需要按行重新整理数据,把粘在一起的数据分开
            managedData = []
            for key in sortedKeys:
                quadList = dataTable[key]
                rowStrList = []
               
                for num in range(0, len(quadList)):
                    print(quadList[num].words)
                    lastStartIndex = 0
                    if len(quadList[num].chars) == 1:
                        cq = playerResult.contentQuad()
                        cq.words = quadList[num].words[lastStartIndex:]
                        print('common add:' + cq.words)
                        cq.chars = quadList[num].chars[lastStartIndex:]
                        cq.leftAnchor = quadList[num].chars[lastStartIndex]['location']['left']
                        rowStrList.append(cq)
                        continue
                    for charIndex in range(0, len(quadList[num].chars) - 1):
                        interval = quadList[num].chars[charIndex + 1]['location']['left'] -  quadList[num].chars[charIndex]['location']['left']
                        width = quadList[num].chars[charIndex]['location']['width']
                        if interval > width * 3:
                            #找到空隙
                             cq = playerResult.contentQuad()
                             cq.words = quadList[num].words[lastStartIndex:charIndex + 1]
                             print('find gap:' + cq.words)
                             cq.chars = quadList[num].chars[lastStartIndex:charIndex + 1]
                             cq.leftAnchor = quadList[num].chars[lastStartIndex]['location']['left']
                             lastStartIndex = charIndex + 1
                             rowStrList.append(cq)
                             if charIndex == len(quadList[num].chars) - 2:
                                 cq = playerResult.contentQuad()
                                 cq.words = quadList[num].words[lastStartIndex:]
                                 print('common add:' + cq.words)
                                 cq.chars = quadList[num].chars[lastStartIndex:]
                                 cq.leftAnchor = quadList[num].chars[lastStartIndex]['location']['left']
                                 rowStrList.append(cq)
                        elif charIndex == len(quadList[num].chars) - 2:
                            cq = playerResult.contentQuad()
                            cq.words = quadList[num].words[lastStartIndex:]
                            print('common add:' + cq.words)
                            cq.chars = quadList[num].chars[lastStartIndex:]
                            cq.leftAnchor = quadList[num].chars[lastStartIndex]['location']['left']
                            rowStrList.append(cq)
                managedData.append(rowStrList)   
            
           

            #坐标信息
            playerNameLeftPos = 0
            playerIDLeftPos = 0
            playerScoreLeftPos = 0

            playerNameRightPos = 0  #方向不是正常方向的时候 才用的得到
            playerIDRightPos = 0    #方向不是正常方向的时候 才用的得到
            playerScoreRightPos = 0 #方向不是正常方向的时候 才用的得到

            wholeScoreSum = 0       #先获取所有分数的和，除以2就是赢的总数或者输的总数
            room_data = playerResult.roomData()

            findTitle = False
            titleRowIndex = 0
            addedPlayer = 0
            findHosterProgress = 0
            IDCharacterWidth = 30
            wrong_img = False
            startTime = None
            #开始抓取信息
            for num in range(0, len(managedData)):
                if findTitle == False:
                    if len(managedData[num]) >= 2:
                        for quadIndex in range(0, len(managedData[num]) - 1):
                            if '房号' in managedData[num][quadIndex].words or '房' in managedData[num][quadIndex].words:
                                findTitle = True
                                titleRowIndex = num
                                roomId, roomHoster = getRoomIDAndHoster(managedData[num], quadIndex)
                                room_data.roomId = roomId
                                room_data.roomHoster = roomHoster
                                break
                            else:
                                continue

                elif num == titleRowIndex + 1:
                    #局数和开始时间
                    roundNumber, startTime, playerIDLeftPos = getRoundNumberAndStartTime(managedData[num])
                    room_data.roundCounter = roundNumber
                    room_data.startTime = startTime
                elif num == titleRowIndex + 2:
                    #昵称 ID 得分的起始坐标。
                    if len(managedData[num]) == 3:
                        playerNameLeftPos = int(managedData[num][0].leftAnchor) + 2 * int(managedData[num][0].chars[0]['location']['width']) + 10
                        playerIDLeftPos = int(managedData[num][1].leftAnchor)
                        playerScoreLeftPos = int(managedData[num][2].leftAnchor)
                    elif len(managedData[num]) == 2:
                        if playerIDLeftPos == 0:
                            wrong_img = True
                            self.itchat_instance.send('图片识别错误1', 'filehelper')
                            break
                elif len(managedData[num]) == 2:
                #开始抓用户分数数据
                    if abs(managedData[num][0].leftAnchor - playerIDLeftPos) < IDCharacterWidth:
                        playerId = int(managedData[num][0].words)
                        if findHosterProgress == 1:
                            room_data.roomHosterId = playerId
                            findHosterProgress = 2
                        score = abs(int(managedData[num][1].words)) 
                        wholeScoreSum = wholeScoreSum + score
                        playerData = playerResult.playerData()
                        playerData.name = ''
                        playerData.id = playerId
                        playerData.score = score
                        room_data.playerData.append(playerData)
                        addedPlayer = addedPlayer + 1
                        if addedPlayer == 9:
                            break
                    else:
                        if managedData[num][0].leftAnchor < playerNameLeftPos:
                            self.itchat_instance.send('检测到没用的字符识别', 'filehelper')
                            continue
                        else:
                            print('length 2---leftAnchor:' + str(managedData[num][0].leftAnchor)+', playerIDLeftPos:' + str(playerIDLeftPos))
                            wrong_img = True
                            self.itchat_instance.send('图片识别错误2', 'filehelper')
                            break
                elif len(managedData[num]) == 3:
                    if abs(managedData[num][1].leftAnchor - playerIDLeftPos) < IDCharacterWidth:
                        playerId = int(managedData[num][1].words)
                        if findHosterProgress == 1:
                            room_data.roomHosterId = playerId
                            findHosterProgress = 2
                        score = abs(int(managedData[num][2].words)) 
                        nickName = managedData[num][0].words
                        wholeScoreSum = wholeScoreSum + score
                        playerData = playerResult.playerData()
                        playerData.name = nickName
                        playerData.id = playerId
                        playerData.score = score
                        room_data.playerData.append(playerData)
                        addedPlayer = addedPlayer + 1
                        if addedPlayer == 9:
                            break
                    else:
                        print('length 3---leftAnchor:' + str(managedData[num][1].leftAnchor)+', playerIDLeftPos:' + str(playerIDLeftPos))
                        wrong_img = True
                        self.itchat_instance.send('图片识别错误3', 'filehelper')
                        break
                elif len(managedData[num]) > 3:
                    for index in range(0,len(managedData[num])):
                        if abs(managedData[num][index].leftAnchor - playerIDLeftPos) < IDCharacterWidth and index > 0:
                            #find the id
                            playerId = int(managedData[num][index].words)
                            if findHosterProgress == 1:
                                room_data.roomHosterId = playerId
                                findHosterProgress = 2
                            score = abs(int(managedData[num][index + 1].words)) 
                            nickName = managedData[num][index - 1].words
                            wholeScoreSum = wholeScoreSum + score
                            playerData = playerResult.playerData()
                            playerData.name = nickName
                            playerData.id = playerId
                            playerData.score = score
                            room_data.playerData.append(playerData)
                            addedPlayer = addedPlayer + 1
                            break
                    if addedPlayer == 9:
                        break
                    print('length more not even one match')
                elif len(managedData[num]) == 1:
                    if '房主' in managedData[num][0].words or '房' in managedData[num][0].words:
                        #找到房主这一行
                        if findHosterProgress == 0:
                            findHosterProgress = 1
                        else :
                            print('hoster wrong')
                            wrong_img = True
                            self.itchat_instance.send('图片识别错误4', 'filehelper')
                            break
                            
            if wrong_img or room_data.startTime == '' or room_data.roomId == 0\
                     or room_data.roundCounter == 0 or len(room_data.playerData) == 0:
                erro_msg = '图片无法识别\n'
                erro_msg+= 'roomId:' + str(room_data.roomId) + '\n'
                erro_msg+= 'startTime:' + str(room_data.startTime) + '\n'
                erro_msg+= 'roomHosterId:' + str(room_data.roomHosterId) + '\n'
                erro_msg+= 'roomHoster:' + str(room_data.roomHoster) + '\n'
                erro_msg+= 'roundCounter:' + str(room_data.roundCounter) + '\n'
                erro_msg+= 'players:' + str(len(room_data.playerData))

                wrong_image = WrongImage(club_name=clubInstance.user_name, image=msg.fileName, create_time=int(time.time()))
                wrong_image.save()
                self.itchat_instance.send(erro_msg, 'filehelper')
                return
            #计算玩家分数正负号
            wholeScoreSum = wholeScoreSum / 2
            for num in range(0, len(room_data.playerData)) :

                if wholeScoreSum > 0:
                    wholeScoreSum = wholeScoreSum - room_data.playerData[num].score
                else:
                    room_data.playerData[num].score = -room_data.playerData[num].score
            
            try:
                print('roomId:'+str(room_data.roomId)+',startTime:'+str(startTime))
                HistoryGame.objects.get(club_id=clubInstance.uuid, round_number=room_data.roundCounter, room_id=room_data.roomId, start_time=startTime)
                self.itchat_instance.send('数据已入库！', 'filehelper')      
                return ''
            except HistoryGame.DoesNotExist:
                playerData = []
                for d in room_data.playerData:
                    playerData.append(d.dumps())
                historyGame = HistoryGame(club=clubInstance, room_id=room_data.roomId, hoster_name=room_data.roomHoster,\
                hoster_id=room_data.roomHosterId, round_number=room_data.roundCounter, start_time=room_data.startTime, \
                player_data=json.dumps(playerData), create_time=timezone.now())
                historyGame.save()
                room_data.toString()
                pic_msg = '房间ID：' + str(room_data.roomId) + '\n'
                pic_msg+= '房主：' + str(room_data.roomHoster) + '\n'
                pic_msg+= '房主ID：' + str(room_data.roomHosterId) + '\n'
                pic_msg+= '局数：' + str(room_data.roundCounter) + '\n'
                pic_msg+= '开始时间：' + str(room_data.startTime) + '\n'
                pic_msg+= '-------------------------------------\n'
                '''
                self.itchat_instance.send('房间ID：' + str(room_data.roomId), 'filehelper')
                self.itchat_instance.send('房主：' + str(room_data.roomHoster), 'filehelper')
                self.itchat_instance.send('房主ID：' + str(room_data.roomHosterId), 'filehelper')
                self.itchat_instance.send('局数：' + str(room_data.roundCounter), 'filehelper')
                self.itchat_instance.send('开始时间：' + str(room_data.startTime), 'filehelper') 
                '''
                rules = []
                clubInstance = Clubs.objects.get(user_name=clubInstance.user_name)
                if clubInstance.cost_param == None or clubInstance.cost_param == 'none' or clubInstance.cost_param == '':
                    pass
                else:
                    rules = clubInstance.cost_param
                    rules = rules.split('|')
                costMode = clubInstance.cost_mode

                clubProfit = 0
                
                for num in range(0, len(room_data.playerData)):
                    costed = False
                    gameid = None
                    player = None
                    wechat_uuid = None

                    playserScore = room_data.playerData[num].score 
                    is_host = 0
                    if room_data.playerData[num].name == room_data.roomHoster:
                        is_host = 1
                    try:
                        gameid = GameID.objects.get(club=clubInstance, gameid=room_data.playerData[num].id)
                        player = gameid.player
                        f = self.itchat_instance.search_friends(remarkName=player.nick_name)
                        print('friends111......')
                        print(f)
                        print('..............')
                        if f:
                            if isinstance(f,list):
                                wechat_uuid = f[0]['UserName']
                            elif isinstance(f,dict):
                                wechat_uuid = f['UserName']

                    except GameID.DoesNotExist:
                        self.itchat_instance.send('用户id：' + str(room_data.playerData[num].id) + '没有注册, 创建临时账号：tempUser', 'filehelper')
                        player = Player(wechat_nick_name='tempUser', nick_name=room_data.playerData[num].name, club=clubInstance, current_score=0, history_profit=0)
                        player.save()
                        gameid = GameID(club=clubInstance, player=player, gameid=room_data.playerData[num].id, game_nick_name=room_data.playerData[num].name)
                        gameid.save()
                    if is_host:
                        player.today_hoster_number += 1
                    try:
                        last_current_score = player.current_score;

                        if len(rules) > 0:
                            if costMode == 0 and num < int(rules[0]):
                                #固定模式 3|20_15_10|100
                                value = int(rules[2])
                                params = rules[1].split('_')
                                cost = int(params[num])

                                if playserScore > value:
                                    score = Score(player=player, score=playserScore - cost, cost=cost, is_host=is_host, create_time=timezone.now(), room_id=room_data.roomId)
                                    score.save()
                                    player.current_score = player.current_score + room_data.playerData[num].score - cost 
                                    player.history_profit = player.history_profit + room_data.playerData[num].score - cost
                                    player.history_cost += cost
                                    player.save()
                                    historyGame.cost += cost
                                    historyGame.score += room_data.playerData[num].score - cost
                                    costed = True
                                    clubProfit += cost
                                    pic_msg+= str(num+1) + '.ID' + str(room_data.playerData[num].id) + '：' + player.nick_name + '  分数：' + str(room_data.playerData[num].score) + \
                                    '  管理费：' + str(cost) + '  总分数：' + str(player.current_score) + '\n'
                                    #self.itchat_instance.send('玩家id：' + str(room_data.playerData[num].id) + '  分数：' + str(room_data.playerData[num].score) + \
                                    #'  管理费：' + str(cost) + '  总分数：' + str(player.current_score), 'filehelper')    
                                    if wechat_uuid:
                                        self.itchat_instance.send_image(img_file, wechat_uuid)
                                        alert_msg = player.nick_name + '\n'
                                        alert_msg+= '上次积分: '+str(last_current_score) + '\n'
                                        alert_msg+= '本局积分: '+str(room_data.playerData[num].score) + '\n'
                                        alert_msg+= '本局房费: '+str(cost) + '\n'
                                        alert_msg+= '当前余分: '+str(player.current_score) + '\n'
                                        self.itchat_instance.send(alert_msg, wechat_uuid)
                            elif costMode == 1 and num < int(rules[0]):
                                #百分比模式
                                if playserScore >= 100 :
                                    params = rules[1].split('_')
                                    param = float(params[num])
                                    cost = int(playserScore * param)
                                    score = Score(player=player, score=playserScore - cost, cost=cost, is_host=is_host, create_time=timezone.now(), room_id=room_data.roomId)
                                    score.save()
                                    player.current_score = player.current_score + room_data.playerData[num].score - cost 
                                    player.history_profit = player.history_profit + room_data.playerData[num].score - cost
                                    player.history_cost += cost
                                    player.save()
                                    historyGame.cost += cost
                                    historyGame.score += room_data.playerData[num].score - cost
                                    costed = True
                                    clubProfit += cost
                                    pic_msg+= str(num+1) + '.ID' + str(room_data.playerData[num].id) + '：' + player.nick_name + '  分数：' + str(room_data.playerData[num].score) + \
                                    '  管理费：' + str(cost) + '  总分数：' + str(player.current_score) + '\n'
                                    #self.itchat_instance.send('玩家id：' + str(room_data.playerData[num].id) + '  分数：' + str(room_data.playerData[num].score) + \
                                    #'  管理费：' + str(cost) + '  总分数：' + str(player.current_score), 'filehelper') 
                                    if wechat_uuid:
                                        self.itchat_instance.send_image(img_file, wechat_uuid)
                                        alert_msg = player.nick_name + '\n'
                                        alert_msg+= '上次积分: '+str(last_current_score) + '\n'
                                        alert_msg+= '本局积分: '+str(room_data.playerData[num].score) + '\n'
                                        alert_msg+= '本局房费: '+str(cost) + '\n'
                                        alert_msg+= '当前余分: '+str(player.current_score) + '\n'
                                        self.itchat_instance.send(alert_msg, wechat_uuid)
                            elif costMode == 2:
                                values = rules[0].split('_')
                                costs = rules[1].split('_')
                                can_cost = False
                                for index, value in enumerate(values):
                                    if playserScore >= int(value):
                                        can_cost = True
                                        break

                                #所有固定模式
                                if can_cost:
                                    cost = int(costs[index])
                                    score = Score(player=player, score=playserScore - cost, cost=cost, is_host=is_host, create_time=timezone.now(), room_id=room_data.roomId)
                                    score.save()
                                    player.current_score = player.current_score + room_data.playerData[num].score - cost 
                                    player.history_profit = player.history_profit + room_data.playerData[num].score - cost
                                    player.history_cost += cost
                                    player.save()
                                    historyGame.cost += cost
                                    historyGame.score += room_data.playerData[num].score - cost
                                    costed = True
                                    clubProfit += cost
                                    pic_msg+= str(num+1) + '.ID' + str(room_data.playerData[num].id) + '：' + player.nick_name + '  分数：' + str(room_data.playerData[num].score) + \
                                    '  管理费：' + str(cost) + '  总分数：' + str(player.current_score) + '\n'
                                    #self.itchat_instance.send('玩家id：' + str(room_data.playerData[num].id) + '  分数：' + str(room_data.playerData[num].score) + \
                                    #'  管理费：' + str(cost) + '  总分数：' + str(player.current_score), 'filehelper') 
                                    if wechat_uuid:
                                        self.itchat_instance.send_image(img_file, wechat_uuid)
                                        alert_msg = player.nick_name + '\n'
                                        alert_msg+= '上次积分: '+str(last_current_score) + '\n'
                                        alert_msg+= '本局积分: '+str(room_data.playerData[num].score) + '\n'
                                        alert_msg+= '本局房费: '+str(cost) + '\n'
                                        alert_msg+= '当前余分: '+str(player.current_score) + '\n'
                                        self.itchat_instance.send(alert_msg, wechat_uuid)

                        if costed == False:
                            score = Score(player=player, score=playserScore, cost=0, is_host=is_host, create_time=timezone.now(), room_id=room_data.roomId)
                            score.save()
                            player.current_score = player.current_score + room_data.playerData[num].score 
                            player.history_profit = player.history_profit + room_data.playerData[num].score
                            player.save()
                            pic_msg+= str(num+1) + '.ID' + str(room_data.playerData[num].id) + '：' + player.nick_name + '  分数：' + str(room_data.playerData[num].score) + \
                            '  总分数：' + str(player.current_score) + '\n'
                            #self.itchat_instance.send('玩家id：' + str(room_data.playerData[num].id) + '  分数：' + str(room_data.playerData[num].score) + \
                            #'  总分数：' + str(player.current_score), 'filehelper')      
                            if wechat_uuid:
                                self.itchat_instance.send_image(img_file, wechat_uuid)
                                alert_msg = player.nick_name + '\n'
                                alert_msg+= '上次积分: '+str(last_current_score) + '\n'
                                alert_msg+= '本局积分: '+str(room_data.playerData[num].score) + '\n'
                                alert_msg+= '本局房费: 无' + '\n'
                                alert_msg+= '当前余分: '+str(player.current_score) + '\n'
                                self.itchat_instance.send(alert_msg, wechat_uuid)
                        #授信
                        print('score_limit==============' + wechat_uuid + '--' + str(player.score_limit) + '--' + str(player.current_score) + '--' + str(player.score_limit))
                        if wechat_uuid and player.score_limit !=0 and player.current_score <= player.score_limit:
                            alert_msg = player.nick_name + '\n'
                            alert_msg+= '上分提醒\n'
                            alert_msg+= '当前余分: '+str(player.current_score) + '\n'
                            alert_msg+= player.score_limit_desc + '\n'
                            self.itchat_instance.send(alert_msg, wechat_uuid)
                    except:
                        traceback.print_exc()
                        self.itchat_instance.send('发生异常！', 'filehelper')
                        continue
                historyGame.save()        
          
            clubInstance.profit += clubProfit
            clubInstance.save()
            pic_msg+= '-------------------------------------\n'
            pic_msg+= '获得管理费：' + str(clubProfit)
            self.itchat_instance.send(pic_msg, 'filehelper') 
            return '@%s@%s' % (typeSymbol, msg.fileName)


        # 接受图片的逻辑处理
        @self.itchat_instance.msg_register([PICTURE])
        def download_files_new(msg):
            clubInstance = Clubs.objects.get(user_name=self.club.user_name)
            if clubInstance.expired_time < time.time():
                self.itchat_instance.send('CD KEY 已失效。 请延长后继续使用。', 'filehelper')
                self.itchat_instance.logout()
                return

            if msg['ToUserName'] != 'filehelper':
                return

            self.itchat_instance.send('正在识别...', 'filehelper')

            club_path = settings.STATIC_ROOT + '/upload/' + clubInstance.user_name + '/'
            if not os.path.exists(club_path):
                os.mkdir(club_path)
            img_file = club_path + msg.fileName
            msg.download(img_file)
            typeSymbol = {
                PICTURE: 'img',
                }.get(msg.type, 'fil')

            # 从识别的文本中抓取最终结果
            result = aipOcr.accurate(get_file_content(img_file), options)
            resultDir = result['direction']#0:是正常方向，3是顺时针90度
            wordsArray = result['words_result']
            room_data = get_pic_info(wordsArray)
            total_score = 0
            for playerData in room_data.playerData:
                total_score += playerData.score

            # # 网络图片文字文字识别接口
            # tempAry = ["64809cb9569bd1f748cf42344ba736fe", "e795a6b645d872e6e093550c9393b845"]
            # # result = aipOcr.accurate(get_file_content(img_file),options)
            # for tempSign in tempAry:
            #     result = aipOcr.custom(get_file_content(img_file), tempSign)
            #     if result["error_code"] == 17:
            #         erro_msg = '百度识别次数达到上限，请联系管理员'
            #         self.itchat_instance.send(erro_msg, 'filehelper')
            #         return
            #     if result["error_code"] == 272000:
            #     #     模板不匹配
            #         continue
            #     try:
            #         print("log_id: %s" % result["data"]["logId"])
            #         room_data = get_template_pic_info(result["data"]["ret"])
            #         if len(room_data.playerData) > 9:
            #             erro_msg = '识别用户超过9个，请联系管理员'
            #             self.itchat_instance.send(erro_msg, 'filehelper')
            #             return
            #         total_score = 0
            #         for playerData in room_data.playerData:
            #             total_score += playerData.score
            #         break
            #     except:
            #         erro_msg = '图片无法识别\n请试着上传原图，或者联系管理员'
            #         self.itchat_instance.send(erro_msg, 'filehelper')
            #         return


            if room_data.startTime == '' or room_data.roomId == 0 or total_score != 0\
                     or room_data.roundCounter == 0 or len(room_data.playerData) == 0:
                erro_msg = '图片无法识别\n'
                erro_msg+= 'roomId:' + str(room_data.roomId) + '\n'
                erro_msg+= 'startTime:' + str(room_data.startTime) + '\n'
                erro_msg+= 'roomHosterId:' + str(room_data.roomHosterId) + '\n'
                erro_msg+= 'roomHoster:' + str(room_data.roomHoster) + '\n'
                erro_msg+= 'roundCounter:' + str(room_data.roundCounter) + '\n'
                erro_msg+= 'players:' + str(len(room_data.playerData)) + '\n'
                erro_msg+= 'total_score:' + str(total_score) + '\n'
                erro_msg += '请试着上传原图，或者联系管理员'

                wrong_image = WrongImage(club_name=clubInstance.user_name, image=msg.fileName, create_time=int(time.time()))
                wrong_image.save()
                self.itchat_instance.send(erro_msg, 'filehelper')
                return
            #根据刷新时间设置，设置入库时间
            today_time_start = '%s-%s-%s 0:0:0' % (timezone.now().year, timezone.now().month, timezone.now().day)
            timeArray = time.strptime(today_time_start, "%Y-%m-%d %H:%M:%S")
            today_time_start = int(time.mktime(timeArray))

            refresh_time = timezone.now()
            if time.time() < today_time_start + clubInstance.refresh_time * 3600:
                refresh_time = timezone.now() - datetime.timedelta(days=1)
            try:
                HistoryGame.objects.get(club_id=clubInstance.uuid, room_id=room_data.roomId, start_time=room_data.startTime)
                self.itchat_instance.send('数据已入库！', 'filehelper')      
                return ''
            except HistoryGame.DoesNotExist:
                playerData = []
                for d in room_data.playerData:
                    playerData.append(d.dumps())
                historyGame = HistoryGame(club=clubInstance, room_id=room_data.roomId, hoster_name=room_data.roomHoster,\
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
                '''
                self.itchat_instance.send('房间ID：' + str(room_data.roomId), 'filehelper')
                self.itchat_instance.send('房主：' + str(room_data.roomHoster), 'filehelper')
                self.itchat_instance.send('房主ID：' + str(room_data.roomHosterId), 'filehelper')
                self.itchat_instance.send('局数：' + str(room_data.roundCounter), 'filehelper')
                self.itchat_instance.send('开始时间：' + str(room_data.startTime), 'filehelper') 
                '''
                #管理员
                manager_wechat_uuids = []
                for manager in Manager.objects.filter(club=clubInstance):
                    f = self.itchat_instance.search_friends(remarkName=manager.nick_name)
                    if f:
                        if isinstance(f,list):
                            manager_wechat_uuids.append(f[0]['UserName'])
                        elif isinstance(f,dict):
                            manager_wechat_uuids.append(f['UserName'])

                rules = []
                if clubInstance.cost_param == None or clubInstance.cost_param == 'none' or clubInstance.cost_param == '':
                    pass
                else:
                    rules = clubInstance.cost_param
                    rules = rules.split('|')
                costMode = clubInstance.cost_mode

                clubProfit = 0
                
                for num in range(0, len(room_data.playerData)):
                    costed = False
                    gameid = None
                    player = None
                    wechat_uuid = None
                    has_gameid = False

                    playserScore = room_data.playerData[num].score 
                    is_host = 0
                    if room_data.playerData[num].name == room_data.roomHoster:
                        is_host = 1

                    gameids = GameID.objects.filter(club=clubInstance, gameid=room_data.playerData[num].id)
                    for gameid in gameids:
                        try:
                            player = Player.objects.get(id=gameid.player_id, is_del=0)
                            f = self.itchat_instance.search_friends(remarkName=player.nick_name)
                            print('friends......')
                            print(f)
                            print('..............')
                            if f:
                                if isinstance(f,list):
                                    wechat_uuid = f[0]['UserName']
                                elif isinstance(f,dict):
                                    wechat_uuid = f['UserName']
                            has_gameid = True
                            break
                        except Player.DoesNotExist:
                            pass

                    if not has_gameid:
                        self.itchat_instance.send('用户id：' + str(room_data.playerData[num].id) + '没有注册, 创建临时账号：' + room_data.playerData[num].name, 'filehelper')
                        player = Player(wechat_nick_name=room_data.playerData[num].name, nick_name=room_data.playerData[num].name, club=clubInstance, current_score=0, history_profit=0)
                        player.save()
                        gameid = GameID(club=clubInstance, player=player, gameid=room_data.playerData[num].id, game_nick_name=room_data.playerData[num].name)
                        gameid.save()

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
                                    cost = int(playserScore * float(params[num]))

                                if playserScore > value:
                                    score = Score(player=player, score=playserScore - cost, cost=cost, is_host=is_host, create_time=timezone.now(), room_id=room_data.roomId, refresh_time=refresh_time)
                                    score.save()
                                    player.current_score = player.current_score + room_data.playerData[num].score - cost 
                                    player.history_profit = player.history_profit + room_data.playerData[num].score - cost
                                    player.history_cost += cost
                                    player.save()
                                    historyGame.cost += cost
                                    historyGame.score += room_data.playerData[num].score - cost
                                    costed = True
                                    clubProfit += cost
                                    pic_msg+= str(num+1) + '.ID' + str(room_data.playerData[num].id) + '：' + player.nick_name + '  分数：' + str(room_data.playerData[num].score) + \
                                    '  管理费：' + str(cost) + '  总分数：' + str(player.current_score) + '\n'
                                    #self.itchat_instance.send('玩家id：' + str(room_data.playerData[num].id) + '  分数：' + str(room_data.playerData[num].score) + \
                                    #'  管理费：' + str(cost) + '  总分数：' + str(player.current_score), 'filehelper')    
                                    if wechat_uuid:
                                        self.itchat_instance.send_image(img_file, wechat_uuid)
                                        alert_msg = player.nick_name + '\n'
                                        alert_msg+= '上次积分: '+str(last_current_score) + '\n'
                                        alert_msg+= '本局积分: '+str(room_data.playerData[num].score) + '\n'
                                        alert_msg+= '本局房费: '+str(cost) + '\n'
                                        alert_msg+= '当前余分: '+str(player.current_score) + '\n'
                                        self.itchat_instance.send(alert_msg, wechat_uuid)
                            elif costMode == 1 and num < int(rules[0]):
                                ranges = rules[1].split('*')
                                costs = rules[2].split('*')
                                cost = 0
                                for index, range_ in enumerate(ranges):
                                    if num == index:
                                        costs_ = costs[index].split('_')
                                        for rindex, rrange_ in enumerate(range_.split('_')):
                                            if playserScore < int(rrange_):
                                                cost = int(costs_[rindex])
                                                break
                                if cost > 0:
                                    score = Score(player=player, score=playserScore - cost, cost=cost, is_host=is_host, create_time=timezone.now(), room_id=room_data.roomId, refresh_time=refresh_time)
                                    score.save()
                                    player.current_score = player.current_score + room_data.playerData[num].score - cost 
                                    player.history_profit = player.history_profit + room_data.playerData[num].score - cost
                                    player.history_cost += cost
                                    player.save()
                                    historyGame.cost += cost
                                    historyGame.score += room_data.playerData[num].score - cost
                                    costed = True
                                    clubProfit += cost
                                    pic_msg+= str(num+1) + '.ID' + str(room_data.playerData[num].id) + '：' + player.nick_name + '  分数：' + str(room_data.playerData[num].score) + \
                                    '  管理费：' + str(cost) + '  总分数：' + str(player.current_score) + '\n'
                                    #self.itchat_instance.send('玩家id：' + str(room_data.playerData[num].id) + '  分数：' + str(room_data.playerData[num].score) + \
                                    #'  管理费：' + str(cost) + '  总分数：' + str(player.current_score), 'filehelper') 
                                    if wechat_uuid:
                                        self.itchat_instance.send_image(img_file, wechat_uuid)
                                        alert_msg = player.nick_name + '\n'
                                        alert_msg+= '上次积分: '+str(last_current_score) + '\n'
                                        alert_msg+= '本局积分: '+str(room_data.playerData[num].score) + '\n'
                                        alert_msg+= '本局房费: '+str(cost) + '\n'
                                        alert_msg+= '当前余分: '+str(player.current_score) + '\n'
                                        self.itchat_instance.send(alert_msg, wechat_uuid)
                            elif costMode == 2:
                                values = rules[0].split('_')
                                costs = rules[1].split('_')
                                can_cost = False
                                for index, value in enumerate(values):
                                    if playserScore >= int(value):
                                        can_cost = True
                                        break

                                #所有固定模式
                                if can_cost:
                                    cost = int(costs[index])
                                    score = Score(player=player, score=playserScore - cost, cost=cost, is_host=is_host, create_time=timezone.now(), room_id=room_data.roomId, refresh_time=refresh_time)
                                    score.save()
                                    player.current_score = player.current_score + room_data.playerData[num].score - cost 
                                    player.history_profit = player.history_profit + room_data.playerData[num].score - cost
                                    player.history_cost += cost
                                    player.save()
                                    historyGame.cost += cost
                                    historyGame.score += room_data.playerData[num].score - cost
                                    costed = True
                                    clubProfit += cost
                                    pic_msg+= str(num+1) + '.ID' + str(room_data.playerData[num].id) + '：' + player.nick_name + '  分数：' + str(room_data.playerData[num].score) + \
                                    '  管理费：' + str(cost) + '  总分数：' + str(player.current_score) + '\n'
                                    #self.itchat_instance.send('玩家id：' + str(room_data.playerData[num].id) + '  分数：' + str(room_data.playerData[num].score) + \
                                    #'  管理费：' + str(cost) + '  总分数：' + str(player.current_score), 'filehelper') 
                                    if wechat_uuid:
                                        self.itchat_instance.send_image(img_file, wechat_uuid)
                                        alert_msg = player.nick_name + '\n'
                                        alert_msg+= '上次积分: '+str(last_current_score) + '\n'
                                        alert_msg+= '本局积分: '+str(room_data.playerData[num].score) + '\n'
                                        alert_msg+= '本局房费: '+str(cost) + '\n'
                                        alert_msg+= '当前余分: '+str(player.current_score) + '\n'
                                        self.itchat_instance.send(alert_msg, wechat_uuid)

                        if costed == False:
                            score = Score(player=player, score=playserScore, cost=0, is_host=is_host, create_time=timezone.now(), room_id=room_data.roomId, refresh_time=refresh_time)
                            score.save()
                            player.current_score = player.current_score + room_data.playerData[num].score 
                            player.history_profit = player.history_profit + room_data.playerData[num].score
                            player.save()
                            pic_msg+= str(num+1) + '.ID' + str(room_data.playerData[num].id) + '：' + player.nick_name + '  分数：' + str(room_data.playerData[num].score) + \
                            '  总分数：' + str(player.current_score) + '\n'
                            #self.itchat_instance.send('玩家id：' + str(room_data.playerData[num].id) + '  分数：' + str(room_data.playerData[num].score) + \
                            #'  总分数：' + str(player.current_score), 'filehelper')      
                            if wechat_uuid:
                                self.itchat_instance.send_image(img_file, wechat_uuid)
                                alert_msg = player.nick_name + '\n'
                                alert_msg+= '上次积分: '+str(last_current_score) + '\n'
                                alert_msg+= '本局积分: '+str(room_data.playerData[num].score) + '\n'
                                alert_msg+= '本局房费: 无' + '\n'
                                alert_msg+= '当前余分: '+str(player.current_score) + '\n'
                                self.itchat_instance.send(alert_msg, wechat_uuid)
                        #授信
                        if  player.score_limit !=0 and player.current_score <= -player.score_limit:
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
          
            clubInstance.profit += clubProfit
            clubInstance.save()
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

    def search_friends_by_nickname(self, wechat_nick_name):
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
        return list_

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


