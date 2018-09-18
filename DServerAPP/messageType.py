import json

SUCCESS = 0
USER_NAME_ALREADY_USED = 10000
PASSWORD_WRONG = 10001

def createMessage(success, messageCode, content):
    jsonData = {'result':success, 'messageCode':messageCode, 'content':content}
    return json.dumps(jsonData)




