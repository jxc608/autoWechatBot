import itchat
from itchat.content import *
import time
import threading
from aip import AipOcr
from .models import *
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
    'detect_direction': 'true',
    'language_type': 'CHN_ENG',
}

def output_info(msg):
    print('[INFO] %s' % msg)

#lock = threading.Lock()

class wechatInstance(threading.Thread):
     def __init__(self,uuid,club):
        threading.Thread.__init__(self)
        self.itchat_instance = itchat.new_instance()
        self.club = club
        waitForConfirm = False
        while 1:
            status = self.itchat_instance.check_login(uuid)
            if status == '200':
                break
            elif status == '201':
                if waitForConfirm:
                    output_info('Please press confirm')
                    waitForConfirm = True
            elif status == '408':
                waitForConfirm = False
        userInfo = self.itchat_instance.web_init()
        self.itchat_instance.show_mobile_login()
        self.itchat_instance.get_contact()
        output_info('Login successfully as %s'%userInfo['User']['NickName'])
        self.itchat_instance.start_receiving()

        # 接受文字命令的 逻辑处理
        @self.itchat_instance.msg_register(itchat.content.TEXT)
        def simple_reply(msg):
            if msg['ToUserName'] == 'filehelper':
                self.itchat_instance.send(msg['Content'],'filehelper')
                if msg['Type'] == 'Text':
                    contentSplit = msg['Content'].split('**')

                    for stringContent in contentSplit:
                        print(stringContent)
                        
                    if contentSplit[0] == '注册':
                         if len(contentSplit) != 2:
                             self.itchat_instance.send('参数错误', msg.fromUserName)   
                             return '命令执行失败: %s' % msg['Content']  

                         try:
                             player = Player.objects.get(wechat_nick_name=contentSplit[1])
                             self.itchat_instance.send('用户:' + contentSplit[1] + ' 已经存在。', msg.fromUserName)
                             return '命令执行失败: %s' % msg['Content']
                         except Player.DoesNotExist:
                             player = Player(wechat_nick_name=contentSplit[1], club=self.club, current_score=0, history_profit=0)
                             player.save()
                             self.itchat_instance.send('注册用户:' + contentSplit[1], msg.fromUserName)
                             return '命令执行完成: %s' % msg['Content']

                    elif contentSplit[0] == '绑定游戏id':
                         if  len(contentSplit) != 4:
                             self.itchat_instance.send('参数错误', msg.fromUserName)   
                             return '命令执行失败: %s' % msg['Content']  

                         try:
                             player = Player.objects.get(wechat_nick_name=contentSplit[1], club__user_name__exact=self.club)
                         except Player.DoesNotExist:
                             player = Player(wechat_nick_name=contentSplit[1], club=self.club, current_score=0, history_profit=0)
                             player.save()
                             self.itchat_instance.send('用户:' + contentSplit[1] + '不存在，请先注册用户', msg.fromUserName)
                             return '命令执行失败: %s' % msg['Content']

                         try:
                             gameID = GameID.objects.get(player__wechat_nick_name__exact=contentSplit[1], gameid=contentSplit[2])
                             self.itchat_instance.send('游戏id已绑定', msg.fromUserName)   
                             return '命令执行失败: %s' % msg['Content']  
                         except GameID.DoesNotExist:
                             player = Player.objects.get(wechat_nick_name=contentSplit[1])
                             gameID = GameID(player=player, gameid=contentSplit[2], game_nick_name=contentSplit[3])
                             gameID.save()
                             self.itchat_instance.send('游戏id绑定成功', msg.fromUserName)   
                             return '命令执行成功: %s' % msg['Content']     
                    elif contentSplit[0] == '上分':
                         self.itchat_instance.send('上分:' + contentSplit[1], msg.fromUserName)
                    elif contentSplit[0] == '下分':
                         self.itchat_instance.send('下分:' + contentSplit[1], msg.fromUserName)
                    elif contentSplit[0] == '查看单个用户战绩':
                         self.itchat_instance.send('查看单个用户战绩:' + contentSplit[1], msg.fromUserName)
                    elif contentSplit[0] == '查看所有战绩':
                         self.itchat_instance.send('查看所有战绩:' + contentSplit[1], msg.fromUserName)
                    elif contentSplit[0] == '设置手续费模式':
                         self.itchat_instance.send('设置手续费模式:' + contentSplit[1], msg.fromUserName)
                    elif contentSplit[0] == '查看整体盈利':
                         self.itchat_instance.send('查看整体盈利:' + contentSplit[1], msg.fromUserName)
                    elif contentSplit[0] == '用户改名':
                         self.itchat_instance.send('查看整体盈利:' + contentSplit[1], msg.fromUserName)
                    elif contentSplit[0] == '自动检测改名':
                         self.itchat_instance.send('查看整体盈利:' + contentSplit[1], msg.fromUserName)
                    elif contentSplit[0] == '新增介绍人':
                         self.itchat_instance.send('新增介绍人:' + contentSplit[1], msg.fromUserName)
                    elif contentSplit[0] == '查看介绍人':
                         self.itchat_instance.send('查看介绍人:' + contentSplit[1], msg.fromUserName)


                    return '命令执行完成: %s' % msg['Content']

        # 接受图片的逻辑处理
        @itchat.msg_register([PICTURE])
        def download_files(msg):
            print('picture')
            msg.download(msg.fileName)
            typeSymbol = {
                PICTURE: 'img',
                }.get(msg.type, 'fil')

            
            # 网络图片文字文字识别接口
            result = aipOcr.basicAccurate(get_file_content(msg.fileName),options)

            #从识别的文本中抓取最终结果
            wordsArray = result['words_result']
            resultList = []
            startAddContent = False
            index = 0
            tempPlayerResult = playerResult.playerResult()
            for item in wordsArray:
                print(item['words'])
                if startAddContent:
                    if index == 0:
                        if item['words'].isdigit():
                            index = 2
                            tempPlayerResult = playerResult.playerResult()
                            tempPlayerResult.name = '玩家'
                            tempPlayerResult.id = item['words']
                        else :
                            if item['words'] == '分享到微信':
                                print('get here')
                                index = 3
                                startAddContent = False
                            else:
                                tempPlayerResult = playerResult.playerResult()
                                tempPlayerResult.name = item['words']
                                index += 1
                    elif index == 1:
                        if item['words'].isdigit():
                            tempPlayerResult.id = item['words']
                            index += 1
                        else:
                            tempPlayerResult.name += item['words']
                    elif index == 2:
                        tempPlayerResult.score = item['words']
                        resultList.append(tempPlayerResult)
                        index = 0
                else:
                    if item['words'] == '积分':
                        startAddContent = True
                
            finalStr = ''
            for item in resultList:
                finalStr +=  item.name + '|' + item.id + '|' + item.score + '==='
            #itchat.send(str(result), msg.fromUserName)
            self.itchat_instance.send(str(result), msg.fromUserName)
            self.itchat_instance.send(finalStr, msg.fromUserName)
            return '@%s@%s' % (typeSymbol, msg.fileName)

     def run(self):
         print('thread start')
         self.itchat_instance.run()


