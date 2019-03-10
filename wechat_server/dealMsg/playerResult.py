# -*- coding: utf-8 -*-

class playerData:
    def __init__(self):
        self.name = '' # 昵称
        self.id = 0  # id
        self.score = 0 # 分数

    def dumps(self):
        return {
            'name':self.name,
            'id':self.id,
            'score':self.score
        }

class roomData:
    def __init__(self):
        self.roomId = 0
        self.roomHoster = ''
        self.roomHosterId = 0
        self.startTime = ''
        self.roundCounter =0
        self.playerData = []
    
    def toString(self):
        print('房间ID：' + str(self.roomId))
        print('房主：' + self.roomHoster)
        print('房主ID：' + str(self.roomHosterId))
        print('局数：' + str(self.roundCounter))
        print('开始时间：' + self.startTime)
        for player in self.playerData:
            print('玩家：' + str(player.id) + '---分数：' + str(player.score))

class contentQuad:
    def __init__(self):
        self.words = ''
        self.chars = []
        self.leftAnchor = 0

class cqList:
    def __init__(self):
        self.list = []