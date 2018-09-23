import json

SUCCESS = 0
USER_NAME_ALREADY_USED = 10000
PASSWORD_WRONG = 10001
CLUB_NOT_EXIST= 10002
CLUB_EXPIRED = 10003

def createMessage(success, messageCode, content):
    jsonData = {'result':success, 'messageCode':messageCode, 'content':content}
    return json.dumps(jsonData)




