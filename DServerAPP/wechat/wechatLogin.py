# -*- coding: UTF-8 -*-  
import itchat, time, sys, os

def initItChatInstance():
    newInstance = itchat.new_instance()
    uuid = open_QR(newInstance)
    waitForConfirm = False
    while 1:
        status = newInstance.check_login(uuid)
        if status == '200':
            break
        elif status == '201':
            if waitForConfirm:
                output_info('Please press confirm')
                waitForConfirm = True
        elif status == '408':
            output_info('Reloading QR Code')
            uuid = open_QR(newInstance)
            waitForConfirm = False
    userInfo = newInstance.web_init()
    #non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    #print(userInfo.translate(non_bmp_map))
    newInstance.show_mobile_login()
    newInstance.get_contact()
    output_info('Login successfully as %s'%userInfo['User']['NickName'])
    newInstance.start_receiving()
    
    resultDic = {'instance':newInstance,'UserName':userInfo['User']['UserName'],'picUUID':uuid}

    return resultDic

 
def output_info(msg):
    print('[INFO] %s' % msg)
 
def open_QR(icInstance):
    for get_count in range(10):
        output_info('Getting uuid')
        uuid = icInstance.get_QRuuid()
        while uuid is None: uuid = icInstance.get_QRuuid();time.sleep(1)
        output_info('Getting QR Code')
        if icInstance.get_QR(uuid,False,os.path.split(os.path.realpath(__file__))[0] + '/QRPics/' + uuid + '.png'): break
        elif get_count >= 9:
            output_info('Failed to get QR Code, please restart the program')
            sys.exit()
    output_info('Please scan the QR Code')
    return uuid