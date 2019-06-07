#coding=utf-8
# pip install baidu-aip
# https://cloud.baidu.com/doc/OCR/OCR-Python-SDK.html#.EC.DF.48.27.9B.69.A4.2C.54.1B.DC.95.67.DB.1D.3C

from aip import AipOcr
import os
import json
import re
from script.img_pre_deal import walk

'''
一个房间由房号（room_id）、房主（hoster）、局数（count）和开始时间（start_time） 还有玩家列表组成
玩家列表包括 name、id、score
'''
class PlayerData():
    def __init__(self, ary):
        self.name = ary[0]
        self.id = ary[1]
        self.score = ary[2]

class RoomData():
    def __init__(self, room_id, hoster, count, start_time, data_ary):
        self.room_id = room_id
        self.hoster = hoster
        self.count = count
        self.start_time = start_time
        self.player_data = [PlayerData(item) for item in data_ary]
        for item in self.player_data:
            if self.hoster == item.name:
                self.hoster_id = item.id
                break

    def scanError(self):
        all_score = 0
        for item in self.player_data:
            all_score += item.score
        if all_score == 0:
            print('success')
        else:
            print('error')

class BaiduOcr():
    app_id = ''
    api_key = ''
    secret_key = ''
    client = None
    # 左边界的偏移量
    left_minus = 15

    def __init__(self, app_id, api_key, secret_key):
        self.app_id = app_id
        self.api_key = api_key
        self.secret_key = secret_key
        self.client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    def get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    def get_ocr_result(self, image):
        """ 如果有可选参数 """
        options = {}
        options["recognize_granularity"] = "small"
        options["detect_direction"] = "false"
        options["vertexes_location"] = "false"
        options["probability"] = "true"

        """ 带参数调用通用文字识别（含位置高精度版） """
        res = self.client.accurate(image, options)
        return res

    def get_words_details(self, words_result):
        # 先按照横坐标，将内容分批放入数组中
        parent_ary = []
        minus_height = 5
        cur_top = 0
        word_details = {}
        for word in words_result:
            words = word['words']
            chars = word['chars']
            word_top = int(word['location']['top'])
            if word_top == 0:
                # 距离顶部为0的，一定是别的字符
                continue
            if abs(word_top - cur_top) > minus_height:
                parent_ary.append([])
                cur_top = word_top
            parent_ary[-1].append(words)
            word_details[words] = chars
        return parent_ary, word_details

    def deal_hongpa(self, ocr_data):
        room_id, hoster, count, start_time, data_ary = 0, '', 0, '', []
        log_id = ocr_data['log_id']
        words_result = ocr_data['words_result']
        parent_ary, word_details = self.get_words_details(words_result)
        # 输出按横坐标划分的数组
        print(parent_ary)
        index = 0
        player_num = 0
        # 确定积分左边界和id左边界
        score_left = 0
        id_left = 0
        key_ary = ['房号:\D*(\d+)\D*房主(.*)', '局数:\D*(\d+)\D*时间:(.*)']
        temp_player_ary = []
        for item in parent_ary:
            if index == 0:
                line_str = ''.join(item)
                first = re.search(key_ary[index], line_str)
                if first:
                    room_id = int(first.group(1))
                    hoster = re.sub('[:：]', '', first.group(2).strip())
                    index += 1
            elif index == 1:
                line_str = ''.join(item)
                second = re.search(key_ary[index], line_str)
                if second:
                    count = int(second.group(1))
                    start_time = second.group(2).strip()
                    index += 1
            elif index == 2:
                if '玩家' in item[0] and '积分' in item[1]:
                    # ID积分项，此处记录积分的左边界
                    jifen_detail = word_details[item[1]]
                    for jifen_item in jifen_detail:
                        if jifen_item['char'] == '积':
                            score_left = int(jifen_item['location']['left']) - self.left_minus
                            break

                    index += 1
            elif index == 3:
                if len(item) == 2:
                    # 正常识别两列，标记idscore的左边界
                    id_score = item[1]
                    if not id_left:
                        id_left = int(word_details[item[1]][0]['location']['left']) - self.left_minus
                elif len(item) == 1:
                    # 名字为空或三者挤到一起
                    name = ''
                    id_score = item[0]
                if not re.search('\d{4,}', re.sub('\D', '', id_score)):
                    # 防止玩家数据中间有别的干扰，去掉非数字后须得有4个以上的数字
                    continue
                # 将用户数据，放入临时list中
                temp_player_ary.append(item)

                player_num += 1
                # 最多9个玩家
                if player_num == 9:
                    break
        for item in temp_player_ary:
            if len(item) == 2:
                name = item[0]
                id_score = item[1]
            else:
                id_score = item[0]
            chars = word_details[id_score]
            name, id, score = self.sep_words(name, id_score, chars, id_left, score_left)
            data_ary.append([name, id, score])
        return room_id, hoster, count, start_time, data_ary

    def sep_words(self, name, id_score, chars, id_left, score_left):
        # 根据每个字符的位置，分割字符串为id和score
        score_done = False
        sep_ary = []
        for rev_index, char in enumerate(reversed(chars)):
            cur_left = int(char['location']['left'])
            if not score_done and cur_left < score_left:
                sep_ary.append(rev_index)
                score_done = True
            elif score_done and cur_left < id_left:
                sep_ary.append(rev_index)
                break
        if len(sep_ary) == 2:
            # 三个都挤一起了
            name = id_score[:-sep_ary[1]]
            id = int(id_score[-sep_ary[1]:-sep_ary[0]])
            score = int(id_score[-sep_ary[0]:])
        else:
            id = int(id_score[:-sep_ary[0]])
            score = int(id_score[-sep_ary[0]:])
        return name, id, score

if __name__ == '__main__':
    APP_ID = '16324083'
    API_KEY = 'KWiQHybQIKjrMQVDNC1DuPaO'
    SECRET_KEY = 'Yq7bEpGLYKhqFDnfamYyOf3wGQDwDIxf'
    filePath = os.path.join(r'D:\Python_Workspace\autoWechatBot\script\img', '11.jpg')
    savePath = os.path.join(r'D:\Python_Workspace\autoWechatBot\script\img', 'temp', '2.png')

    api = BaiduOcr(APP_ID, API_KEY, SECRET_KEY)
    walk(filePath, savePath)
    image = api.get_file_content(savePath)
    ocr_data = api.get_ocr_result(image)
    print(ocr_data)
    # ocr_data = {'log_id': 8996419278007494567, 'words_result_num': 25, 'words_result': [{'chars': [{'char': '我', 'location': {'width': 38, 'top': 0, 'left': 185, 'height': 63}}, {'char': '的', 'location': {'width': 79, 'top': 0, 'left': 222, 'height': 64}}, {'char': '圈', 'location': {'width': 42, 'top': 11, 'left': 392, 'height': 66}}], 'words': '我的圈', 'location': {'width': 482, 'top': 0, 'left': 129, 'height': 97}, 'probability': {'variance': 0.013618, 'average': 0.902712, 'min': 0.738079}}, {'chars': [{'char': '房', 'location': {'width': 20, 'top': 118, 'left': 93, 'height': 34}}, {'char': '号', 'location': {'width': 21, 'top': 118, 'left': 113, 'height': 34}}, {'char': ':', 'location': {'width': 17, 'top': 118, 'left': 130, 'height': 34}}, {'char': '2', 'location': {'width': 17, 'top': 118, 'left': 161, 'height': 34}}, {'char': '0', 'location': {'width': 17, 'top': 118, 'left': 171, 'height': 34}}, {'char': '4', 'location': {'width': 18, 'top': 118, 'left': 192, 'height': 34}}, {'char': '1', 'location': {'width': 17, 'top': 118, 'left': 213, 'height': 34}}, {'char': '3', 'location': {'width': 17, 'top': 118, 'left': 223, 'height': 34}}, {'char': '4', 'location': {'width': 17, 'top': 118, 'left': 243, 'height': 34}}, {'char': '房', 'location': {'width': 21, 'top': 118, 'left': 309, 'height': 34}}, {'char': '主', 'location': {'width': 21, 'top': 118, 'left': 339, 'height': 34}}, {'char': ':', 'location': {'width': 17, 'top': 118, 'left': 356, 'height': 34}}, {'char': '啊', 'location': {'width': 21, 'top': 118, 'left': 380, 'height': 34}}, {'char': '洪', 'location': {'width': 21, 'top': 118, 'left': 411, 'height': 34}}], 'words': '房号:204134房主:啊洪', 'location': {'width': 378, 'top': 118, 'left': 62, 'height': 34}, 'probability': {'variance': 0.022109, 'average': 0.957498, 'min': 0.401254}}, {'chars': [{'char': '局', 'location': {'width': 18, 'top': 161, 'left': 88, 'height': 29}}, {'char': '数', 'location': {'width': 18, 'top': 161, 'left': 114, 'height': 29}}, {'char': ':', 'location': {'width': 15, 'top': 161, 'left': 137, 'height': 29}}, {'char': '1', 'location': {'width': 15, 'top': 161, 'left': 163, 'height': 29}}, {'char': '0', 'location': {'width': 15, 'top': 161, 'left': 172, 'height': 29}}], 'words': '局数:10', 'location': {'width': 131, 'top': 161, 'left': 62, 'height': 29}, 'probability': {'variance': 5e-06, 'average': 0.998422, 'min': 0.994154}}, {'chars': [{'char': '时', 'location': {'width': 17, 'top': 161, 'left': 312, 'height': 29}}, {'char': '间', 'location': {'width': 18, 'top': 161, 'left': 337, 'height': 29}}, {'char': ':', 'location': {'width': 14, 'top': 161, 'left': 361, 'height': 29}}, {'char': '0', 'location': {'width': 15, 'top': 161, 'left': 378, 'height': 29}}, {'char': '5', 'location': {'width': 15, 'top': 161, 'left': 395, 'height': 29}}, {'char': '-', 'location': {'width': 14, 'top': 161, 'left': 413, 'height': 29}}, {'char': '2', 'location': {'width': 14, 'top': 161, 'left': 422, 'height': 29}}, {'char': '4', 'location': {'width': 15, 'top': 161, 'left': 439, 'height': 29}}, {'char': '0', 'location': {'width': 14, 'top': 161, 'left': 465, 'height': 29}}, {'char': '0', 'location': {'width': 15, 'top': 161, 'left': 482, 'height': 29}}, {'char': ':', 'location': {'width': 15, 'top': 161, 'left': 491, 'height': 29}}, {'char': '2', 'location': {'width': 18, 'top': 161, 'left': 503, 'height': 29}}, {'char': '6', 'location': {'width': 15, 'top': 161, 'left': 517, 'height': 29}}], 'words': '时间:05-2400:26', 'location': {'width': 260, 'top': 161, 'left': 277, 'height': 29}, 'probability': {'variance': 0.003226, 'average': 0.98132, 'min': 0.785483}}, {'chars': [{'char': '玩', 'location': {'width': 24, 'top': 209, 'left': 65, 'height': 40}}, {'char': '家', 'location': {'width': 25, 'top': 209, 'left': 113, 'height': 40}}], 'words': '玩家', 'location': {'width': 73, 'top': 209, 'left': 65, 'height': 40}, 'probability': {'variance': 0.0, 'average': 0.999899, 'min': 0.999824}}, {'chars': [{'char': 'I', 'location': {'width': 21, 'top': 207, 'left': 356, 'height': 42}}, {'char': 'D', 'location': {'width': 21, 'top': 207, 'left': 377, 'height': 42}}, {'char': '积', 'location': {'width': 25, 'top': 207, 'left': 458, 'height': 42}}, {'char': '分', 'location': {'width': 25, 'top': 207, 'left': 509, 'height': 42}}], 'words': 'ID积分', 'location': {'width': 180, 'top': 207, 'left': 356, 'height': 42}, 'probability': {'variance': 0.028793, 'average': 0.899332, 'min': 0.605473}}, {'chars': [{'char': '九', 'location': {'width': 23, 'top': 267, 'left': 114, 'height': 38}}, {'char': '妹', 'location': {'width': 23, 'top': 267, 'left': 147, 'height': 38}}, {'char': '2', 'location': {'width': 19, 'top': 267, 'left': 177, 'height': 38}}], 'words': '九妹2', 'location': {'width': 85, 'top': 267, 'left': 114, 'height': 38}, 'probability': {'variance': 0.0, 'average': 0.99899, 'min': 0.998085}}, {'chars': [{'char': '8', 'location': {'width': 16, 'top': 271, 'left': 334, 'height': 32}}, {'char': '3', 'location': {'width': 16, 'top': 271, 'left': 350, 'height': 32}}, {'char': '8', 'location': {'width': 16, 'top': 271, 'left': 368, 'height': 32}}, {'char': '9', 'location': {'width': 16, 'top': 271, 'left': 387, 'height': 32}}, {'char': '8', 'location': {'width': 16, 'top': 271, 'left': 406, 'height': 32}}, {'char': '0', 'location': {'width': 16, 'top': 271, 'left': 425, 'height': 32}}, {'char': '1', 'location': {'width': 16, 'top': 271, 'left': 463, 'height': 32}}, {'char': '6', 'location': {'width': 16, 'top': 271, 'left': 482, 'height': 32}}, {'char': '2', 'location': {'width': 16, 'top': 271, 'left': 501, 'height': 32}}, {'char': '9', 'location': {'width': 16, 'top': 271, 'left': 520, 'height': 32}}], 'words': '8389801629', 'location': {'width': 203, 'top': 271, 'left': 334, 'height': 32}, 'probability': {'variance': 0.0, 'average': 0.99961, 'min': 0.998489}}, {'chars': [{'char': '改', 'location': {'width': 22, 'top': 333, 'left': 114, 'height': 38}}, {'char': '变', 'location': {'width': 22, 'top': 333, 'left': 147, 'height': 38}}, {'char': '未', 'location': {'width': 22, 'top': 333, 'left': 192, 'height': 38}}, {'char': '来', 'location': {'width': 23, 'top': 333, 'left': 214, 'height': 38}}, {'char': '7', 'location': {'width': 19, 'top': 333, 'left': 333, 'height': 38}}, {'char': '1', 'location': {'width': 18, 'top': 333, 'left': 356, 'height': 38}}, {'char': '7', 'location': {'width': 19, 'top': 333, 'left': 367, 'height': 38}}, {'char': '5', 'location': {'width': 18, 'top': 333, 'left': 390, 'height': 38}}, {'char': '2', 'location': {'width': 19, 'top': 333, 'left': 401, 'height': 38}}, {'char': '9', 'location': {'width': 18, 'top': 333, 'left': 424, 'height': 38}}, {'char': '5', 'location': {'width': 18, 'top': 333, 'left': 457, 'height': 38}}, {'char': '4', 'location': {'width': 19, 'top': 333, 'left': 479, 'height': 38}}, {'char': '9', 'location': {'width': 17, 'top': 333, 'left': 502, 'height': 38}}], 'words': '改变未来717529549', 'location': {'width': 405, 'top': 333, 'left': 114, 'height': 38}, 'probability': {'variance': 0.0, 'average': 0.999643, 'min': 0.999212}}, {'chars': [{'char': '丢', 'location': {'width': 23, 'top': 397, 'left': 115, 'height': 39}}, {'char': '失', 'location': {'width': 24, 'top': 397, 'left': 149, 'height': 39}}, {'char': '的', 'location': {'width': 23, 'top': 397, 'left': 185, 'height': 39}}, {'char': '记', 'location': {'width': 23, 'top': 397, 'left': 219, 'height': 39}}, {'char': '忆', 'location': {'width': 23, 'top': 397, 'left': 243, 'height': 39}}, {'char': '8', 'location': {'width': 20, 'top': 397, 'left': 331, 'height': 39}}, {'char': '1', 'location': {'width': 20, 'top': 397, 'left': 354, 'height': 39}}, {'char': '3', 'location': {'width': 20, 'top': 397, 'left': 366, 'height': 39}}, {'char': '6', 'location': {'width': 23, 'top': 397, 'left': 382, 'height': 39}}, {'char': '6', 'location': {'width': 19, 'top': 397, 'left': 413, 'height': 39}}, {'char': '5', 'location': {'width': 19, 'top': 397, 'left': 424, 'height': 39}}, {'char': '2', 'location': {'width': 19, 'top': 397, 'left': 459, 'height': 39}}, {'char': '2', 'location': {'width': 19, 'top': 397, 'left': 482, 'height': 39}}, {'char': '2', 'location': {'width': 14, 'top': 397, 'left': 505, 'height': 39}}], 'words': '丢失的记忆813665222', 'location': {'width': 404, 'top': 397, 'left': 115, 'height': 39}, 'probability': {'variance': 1.9e-05, 'average': 0.997717, 'min': 0.986349}}, {'chars': [{'char': '锦', 'location': {'width': 23, 'top': 463, 'left': 114, 'height': 38}}, {'char': '年', 'location': {'width': 23, 'top': 463, 'left': 147, 'height': 38}}], 'words': '锦年', 'location': {'width': 65, 'top': 463, 'left': 114, 'height': 38}, 'probability': {'variance': 0.0, 'average': 0.999684, 'min': 0.999417}}, {'chars': [{'char': '6', 'location': {'width': 17, 'top': 466, 'left': 334, 'height': 32}}, {'char': '1', 'location': {'width': 16, 'top': 466, 'left': 350, 'height': 32}}, {'char': '8', 'location': {'width': 16, 'top': 466, 'left': 369, 'height': 32}}, {'char': '8', 'location': {'width': 17, 'top': 466, 'left': 388, 'height': 32}}, {'char': '5', 'location': {'width': 17, 'top': 466, 'left': 407, 'height': 32}}, {'char': '2', 'location': {'width': 16, 'top': 466, 'left': 427, 'height': 32}}, {'char': '-', 'location': {'width': 17, 'top': 466, 'left': 455, 'height': 32}}, {'char': '1', 'location': {'width': 17, 'top': 466, 'left': 474, 'height': 32}}, {'char': '4', 'location': {'width': 16, 'top': 466, 'left': 494, 'height': 32}}, {'char': '1', 'location': {'width': 15, 'top': 466, 'left': 513, 'height': 32}}], 'words': '618852-141', 'location': {'width': 194, 'top': 466, 'left': 334, 'height': 32}, 'probability': {'variance': 1e-06, 'average': 0.999437, 'min': 0.997214}}, {'chars': [{'char': '凡', 'location': {'width': 23, 'top': 529, 'left': 147, 'height': 37}}], 'words': '凡', 'location': {'width': 32, 'top': 529, 'left': 147, 'height': 37}, 'probability': {'variance': 0.0, 'average': 0.999966, 'min': 0.999966}}, {'chars': [{'char': '8', 'location': {'width': 16, 'top': 530, 'left': 334, 'height': 33}}, {'char': '0', 'location': {'width': 17, 'top': 530, 'left': 350, 'height': 33}}, {'char': '9', 'location': {'width': 17, 'top': 530, 'left': 370, 'height': 33}}, {'char': '5', 'location': {'width': 17, 'top': 530, 'left': 390, 'height': 33}}, {'char': '4', 'location': {'width': 17, 'top': 530, 'left': 410, 'height': 33}}, {'char': '8', 'location': {'width': 16, 'top': 530, 'left': 430, 'height': 33}}, {'char': '-', 'location': {'width': 17, 'top': 530, 'left': 460, 'height': 33}}, {'char': '2', 'location': {'width': 17, 'top': 530, 'left': 469, 'height': 33}}, {'char': '7', 'location': {'width': 17, 'top': 530, 'left': 489, 'height': 33}}, {'char': '7', 'location': {'width': 17, 'top': 530, 'left': 509, 'height': 33}}], 'words': '809548-277', 'location': {'width': 195, 'top': 530, 'left': 334, 'height': 33}, 'probability': {'variance': 5e-06, 'average': 0.998836, 'min': 0.992223}}, {'chars': [{'char': '啊', 'location': {'width': 33, 'top': 594, 'left': 114, 'height': 20}}, {'char': '一', 'location': {'width': 33, 'top': 639, 'left': 114, 'height': 19}}, {'char': '如', 'location': {'width': 33, 'top': 658, 'left': 114, 'height': 20}}], 'words': '啊一如', 'location': {'width': 33, 'top': 594, 'left': 114, 'height': 101}, 'probability': {'variance': 0.021964, 'average': 0.895152, 'min': 0.68556}}, {'chars': [{'char': '6', 'location': {'width': 16, 'top': 596, 'left': 334, 'height': 32}}, {'char': '8', 'location': {'width': 16, 'top': 596, 'left': 350, 'height': 32}}, {'char': '7', 'location': {'width': 16, 'top': 596, 'left': 369, 'height': 32}}, {'char': '6', 'location': {'width': 16, 'top': 596, 'left': 388, 'height': 32}}, {'char': '6', 'location': {'width': 16, 'top': 596, 'left': 407, 'height': 32}}, {'char': '8', 'location': {'width': 16, 'top': 596, 'left': 426, 'height': 32}}, {'char': '-', 'location': {'width': 20, 'top': 596, 'left': 458, 'height': 32}}, {'char': '3', 'location': {'width': 16, 'top': 596, 'left': 474, 'height': 32}}, {'char': '3', 'location': {'width': 16, 'top': 596, 'left': 493, 'height': 32}}, {'char': '5', 'location': {'width': 16, 'top': 596, 'left': 512, 'height': 32}}], 'words': '687668-335', 'location': {'width': 195, 'top': 596, 'left': 334, 'height': 32}, 'probability': {'variance': 0.000114, 'average': 0.996205, 'min': 0.964172}}, {'chars': [{'char': '此', 'location': {'width': 22, 'top': 659, 'left': 148, 'height': 36}}], 'words': '此', 'location': {'width': 31, 'top': 659, 'left': 148, 'height': 36}, 'probability': {'variance': 0.0, 'average': 0.99972, 'min': 0.99972}}, {'chars': [{'char': '7', 'location': {'width': 17, 'top': 660, 'left': 335, 'height': 35}}, {'char': '7', 'location': {'width': 18, 'top': 660, 'left': 352, 'height': 35}}, {'char': '6', 'location': {'width': 17, 'top': 660, 'left': 373, 'height': 35}}, {'char': '1', 'location': {'width': 17, 'top': 660, 'left': 394, 'height': 35}}, {'char': '9', 'location': {'width': 17, 'top': 660, 'left': 404, 'height': 35}}, {'char': '1', 'location': {'width': 17, 'top': 660, 'left': 425, 'height': 35}}, {'char': '-', 'location': {'width': 18, 'top': 660, 'left': 456, 'height': 35}}, {'char': '3', 'location': {'width': 18, 'top': 660, 'left': 477, 'height': 35}}, {'char': '7', 'location': {'width': 18, 'top': 660, 'left': 488, 'height': 35}}, {'char': '4', 'location': {'width': 17, 'top': 660, 'left': 509, 'height': 35}}], 'words': '776191-374', 'location': {'width': 196, 'top': 660, 'left': 335, 'height': 35}, 'probability': {'variance': 2e-05, 'average': 0.998197, 'min': 0.984763}}, {'chars': [{'char': 'R', 'location': {'width': 19, 'top': 728, 'left': 117, 'height': 29}}, {'char': 'e', 'location': {'width': 23, 'top': 728, 'left': 132, 'height': 29}}, {'char': 'm', 'location': {'width': 25, 'top': 728, 'left': 150, 'height': 29}}, {'char': 'e', 'location': {'width': 28, 'top': 728, 'left': 171, 'height': 29}}, {'char': 'm', 'location': {'width': 25, 'top': 728, 'left': 195, 'height': 29}}, {'char': 'b', 'location': {'width': 23, 'top': 728, 'left': 216, 'height': 29}}], 'words': ' Rememb', 'location': {'width': 131, 'top': 727, 'left': 115, 'height': 32}, 'probability': {'variance': 0.0, 'average': 0.996658, 'min': 0.996658}}, {'chars': [{'char': '8', 'location': {'width': 16, 'top': 726, 'left': 334, 'height': 33}}, {'char': '2', 'location': {'width': 17, 'top': 726, 'left': 350, 'height': 33}}, {'char': '9', 'location': {'width': 17, 'top': 726, 'left': 370, 'height': 33}}, {'char': '4', 'location': {'width': 17, 'top': 726, 'left': 390, 'height': 33}}, {'char': '5', 'location': {'width': 17, 'top': 726, 'left': 410, 'height': 33}}, {'char': '3', 'location': {'width': 17, 'top': 726, 'left': 430, 'height': 33}}, {'char': '-', 'location': {'width': 17, 'top': 726, 'left': 460, 'height': 33}}, {'char': '4', 'location': {'width': 17, 'top': 726, 'left': 470, 'height': 33}}, {'char': '4', 'location': {'width': 17, 'top': 726, 'left': 500, 'height': 33}}, {'char': '1', 'location': {'width': 17, 'top': 726, 'left': 510, 'height': 33}}], 'words': '829453-441', 'location': {'width': 194, 'top': 726, 'left': 334, 'height': 33}, 'probability': {'variance': 6e-06, 'average': 0.998698, 'min': 0.991242}}, {'chars': [{'char': '天', 'location': {'width': 24, 'top': 789, 'left': 124, 'height': 39}}, {'char': '黑', 'location': {'width': 24, 'top': 789, 'left': 148, 'height': 39}}, {'char': '别', 'location': {'width': 24, 'top': 789, 'left': 184, 'height': 39}}, {'char': '出', 'location': {'width': 24, 'top': 789, 'left': 219, 'height': 39}}, {'char': '门', 'location': {'width': 24, 'top': 789, 'left': 244, 'height': 39}}, {'char': '5', 'location': {'width': 19, 'top': 789, 'left': 335, 'height': 39}}, {'char': '4', 'location': {'width': 20, 'top': 789, 'left': 346, 'height': 39}}, {'char': '3', 'location': {'width': 19, 'top': 789, 'left': 371, 'height': 39}}, {'char': '4', 'location': {'width': 20, 'top': 789, 'left': 382, 'height': 39}}, {'char': '9', 'location': {'width': 20, 'top': 789, 'left': 406, 'height': 39}}, {'char': '2', 'location': {'width': 19, 'top': 789, 'left': 430, 'height': 39}}, {'char': '-', 'location': {'width': 20, 'top': 789, 'left': 453, 'height': 39}}, {'char': '8', 'location': {'width': 19, 'top': 789, 'left': 466, 'height': 39}}, {'char': '3', 'location': {'width': 20, 'top': 789, 'left': 489, 'height': 39}}, {'char': '2', 'location': {'width': 17, 'top': 789, 'left': 513, 'height': 39}}], 'words': '天黑别出门543492-832', 'location': {'width': 441, 'top': 789, 'left': 89, 'height': 39}, 'probability': {'variance': 3.3e-05, 'average': 0.997686, 'min': 0.976515}}, {'chars': [{'char': '分', 'location': {'width': 18, 'top': 884, 'left': 166, 'height': 30}}, {'char': '享', 'location': {'width': 18, 'top': 884, 'left': 192, 'height': 30}}, {'char': '到', 'location': {'width': 18, 'top': 884, 'left': 210, 'height': 30}}, {'char': '微', 'location': {'width': 18, 'top': 884, 'left': 237, 'height': 30}}, {'char': '信', 'location': {'width': 18, 'top': 884, 'left': 254, 'height': 30}}, {'char': '分', 'location': {'width': 18, 'top': 884, 'left': 352, 'height': 30}}, {'char': '享', 'location': {'width': 18, 'top': 884, 'left': 369, 'height': 30}}, {'char': '到', 'location': {'width': 18, 'top': 884, 'left': 396, 'height': 30}}, {'char': '默', 'location': {'width': 18, 'top': 884, 'left': 414, 'height': 30}}, {'char': '往', 'location': {'width': 17, 'top': 884, 'left': 440, 'height': 30}}], 'words': '分享到微信分享到默往', 'location': {'width': 291, 'top': 884, 'left': 166, 'height': 30}, 'probability': {'variance': 0.0, 'average': 0.99984, 'min': 0.999279}}, {'chars': [{'char': '查', 'location': {'width': 14, 'top': 877, 'left': 511, 'height': 22}}, {'char': '看', 'location': {'width': 13, 'top': 877, 'left': 537, 'height': 22}}], 'words': '查看', 'location': {'width': 40, 'top': 877, 'left': 511, 'height': 22}, 'probability': {'variance': 0.0, 'average': 0.999959, 'min': 0.999921}}, {'chars': [{'char': '回', 'location': {'width': 13, 'top': 899, 'left': 511, 'height': 21}}, {'char': '放', 'location': {'width': 13, 'top': 899, 'left': 536, 'height': 21}}], 'words': '回放', 'location': {'width': 40, 'top': 899, 'left': 511, 'height': 21}, 'probability': {'variance': 0.0, 'average': 0.999936, 'min': 0.999923}}, {'chars': [{'char': '回', 'location': {'width': 12, 'top': 918, 'left': 38, 'height': 19}}], 'words': '回', 'location': {'width': 19, 'top': 918, 'left': 38, 'height': 19}, 'probability': {'variance': 0.0, 'average': 0.969528, 'min': 0.969528}}]}
    room_id, hoster, count, start_time, data_ary = api.deal_hongpa(ocr_data)
    print(room_id, hoster, count, start_time, data_ary)
    roomData = RoomData(room_id, hoster, count, start_time, data_ary)
    print(roomData.scanError())




