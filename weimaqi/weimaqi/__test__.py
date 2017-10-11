# coding=utf-8
import hashlib
import json
import random

import datetime
import time
from scrapy import cmdline

from items import SettingItem

# 测试读取排除场地信息
# exclude = []
# ch = 'xh'
# if not ch == '':
#     with open("../place.json") as place_file:
#         place = json.load(place_file)
#         place_list = place[ch]
#         if len(place_list) > 0:
#             for p in place_list:
#                 exclude.append(hashlib.md5(p.encode('utf-8')).hexdigest())
#         place_file.close()
# print ('exclude place\n' + str(exclude))

# 密码处理
# print hashlib.md5(hashlib.md5("xxx").hexdigest().upper()).hexdigest()

# 设置爬取
# with open("../account.json") as account_file:
#     load_account = json.load(account_file)
#     cmdline.execute(('scrapy crawl setting -a uid='
#                     + str(load_account[2]['uid'])
#                     + ' -a pwd='
#                     + str(load_account[2]['pwd'])).split())
#     account_file.close()

settings = {}

with open("setting/setting_current.csv") as setting_file:
    i = 0
    invalid = 0
    for line in setting_file:
        if i == 0:
            i = i + 1
            continue
        i = i + 1
        line_d = line.split(',')
        item = SettingItem()
        item['channel'] = line_d[0]
        item['d_name'] = line_d[1]
        item['device_id'] = line_d[2]
        item['tag'] = line_d[3]
        item['des'] = line_d[4]
        item['online'] = line_d[5]
        item['setting_param'] = line_d[6]
        item['coin_per_time'] = line_d[7]
        item['game_duration'] = line_d[8]
        item['music'] = line_d[9]
        item['air_pick'] = line_d[10]
        item['out_pos'] = line_d[11]
        item['shake_clear'] = line_d[12]
        item['music_volume'] = line_d[13]
        item['free_for_continue'] = line_d[14]
        item['strong_force'] = line_d[15]
        item['weak_force'] = line_d[16]
        item['pick_height'] = line_d[17]
        item['strong_to_weak'] = line_d[18]
        item['line_height'] = line_d[19]
        item['out_mode'] = line_d[20]
        item['probability'] = line_d[21]
        item['eyes'] = line_d[22]
        item['keep'] = line_d[23]
        item['account_clear'] = line_d[24]
        item['reset'] = line_d[25]
        item['disable_btn'] = line_d[26]
        item['disable_board'] = line_d[27]
        settings[item['device_id']] = item
        if not item.is_valid():
            invalid = invalid + 1
    print (str(invalid))

