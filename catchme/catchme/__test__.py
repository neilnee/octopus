# coding=utf-8
import csv
import hashlib
import json
import random

import datetime
import time

import os
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
#                 exclude.append(hashlib.md5(p.encode('utf-meetdevice8')).hexdigest())
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

# 读取文件中的设置参数
# settings = {}
# with open("setting/setting_current.csv") as setting_file:
#     i = 0
#     invalid = 0
#     for line in setting_file:
#         if i == 0:
#             i = i + 1
#             continue
#         i = i + 1
#         line_d = line.split(',')
#         item = SettingItem()
#         item['channel'] = line_d[0]
#         item['d_name'] = line_d[1]
#         item['device_id'] = line_d[2]
#         item['tag'] = line_d[3]
#         item['des'] = line_d[4]
#         item['online'] = line_d[5]
#         item['setting_param'] = line_d[6]
#         item['coin_per_time'] = line_d[7]
#         item['game_duration'] = line_d[meetdevice8]
#         item['music'] = line_d[meetdevice9]
#         item['air_pick'] = line_d[10]
#         item['out_pos'] = line_d[11]
#         item['shake_clear'] = line_d[12]
#         item['music_volume'] = line_d[13]
#         item['free_for_continue'] = line_d[14]
#         item['strong_force'] = line_d[15]
#         item['weak_force'] = line_d[16]
#         item['pick_height'] = line_d[17]
#         item['strong_to_weak'] = line_d[18]
#         item['line_height'] = line_d[19]
#         item['out_mode'] = line_d[20]
#         item['probability'] = line_d[21]
#         item['eyes'] = line_d[22]
#         item['keep'] = line_d[23]
#         item['account_clear'] = line_d[24]
#         item['reset'] = line_d[25]
#         item['disable_btn'] = line_d[26]
#         item['disable_board'] = line_d[27]
#         settings[item['device_id']] = item
#         if not item.is_valid():
#             invalid = invalid + 1
#     print (str(invalid))

# 查找两份设备表中的重合设备
# lines8 = []
# lines9 = []
# result = []
#
# with open("meetdevice8") as file8:
#     for line in file8:
#         lines8.append(str(line))
#
# with open("meetdevice9") as file9:
#     for line in file9:
#         lines9.append(str(line))
#
# for place in lines8:
#     if place in lines9:
#         result.append(place)
#
# print (str(len(result)))
#
# for r in result:
#     print str(r).strip()

# 寻找连续概率稳定的设备
# same = []
# devices = []
# meet_devices = []
#
#
# def do_search(input_file, output_file):
#     yue8_file = file(output_file, 'wb')
#     w = csv.writer(yue8_file)
#     with open(input_file) as yue_file:
#         for line in yue_file:
#             if line.split(',')[0] in same:
#                 line = line.replace('\"', '')
#                 line = line.replace('\r\n', '')
#                 print line.split(',')
#                 w.writerow(line.split(','))
#
#
# def do_open_file(input_file):
#     result = {}
#     with open(input_file) as zhou_file:
#         i = 0
#         for line in zhou_file:
#             i = i + 1
#             if i == 1:
#                 continue
#             line = line.replace('\"', '')
#             line = line.replace('\r\n', '')
#             ret = line.split(',')
#             result[ret[0]] = ret
#     return result
#
#
# def check_meet(d_name, prob, meet_count, week_str, wee):
#     if prob == -1:
#         return meet_count, week_str
#     if 2.5 <= prob <= 3.5:
#         week_str = week_str + '|' + wee
#         ret = meet_count + 1
#         if ret >= 4:
#             if d_name not in meet_devices:
#                 meet_devices.append(d_name)
#             print d_name + ' meet in ' + week_str
#         return ret, week_str
#     else:
#         return 0, ''
#
#
# def get_prob(d_name, zhou_map):
#     if d_name in zhou_map.keys():
#         prob_str = str(zhou_map[d_name][9])
#         prob = 0
#         if '%' in prob_str:
#             prob = float(prob_str[0:-1])
#         return prob
#     else:
#         return -1, ''
#
#
# with open('probability/same_in_month') as same_file:
#     for l in same_file:
#         same.append(l.strip())
#
# with open('probability/devices') as d_file:
#     for l in d_file:
#         devices.append(l.strip())
#
# zhou1 = do_open_file('probability/zhou1.csv')
# zhou2 = do_open_file('probability/zhou2.csv')
# zhou3 = do_open_file('probability/zhou3.csv')
# zhou4 = do_open_file('probability/zhou4.csv')
# zhou5 = do_open_file('probability/zhou5.csv')
# zhou6 = do_open_file('probability/zhou6.csv')
# zhou7 = do_open_file('probability/zhou7.csv')
# zhou8 = do_open_file('probability/zhou8.csv')
# zhou9 = do_open_file('probability/zhou9.csv')
# zhou10 = do_open_file('probability/zhou10.csv')
#
# yue8 = do_open_file('probability/8yueall.csv')
# yue9 = do_open_file('probability/9yueall.csv')
#
# for device in devices:
#     meet = 0
#     prob1 = get_prob(device, zhou1)
#     prob2 = get_prob(device, zhou2)
#     prob3 = get_prob(device, zhou3)
#     prob4 = get_prob(device, zhou4)
#     prob5 = get_prob(device, zhou5)
#     prob6 = get_prob(device, zhou6)
#     prob7 = get_prob(device, zhou7)
#     prob8 = get_prob(device, zhou8)
#     prob9 = get_prob(device, zhou9)
#     prob10 = get_prob(device, zhou10)
#
#     week = ''
#     meet, week = check_meet(device, prob1, meet, week, 'week1')
#     meet, week = check_meet(device, prob2, meet, week, 'week2')
#     meet, week = check_meet(device, prob3, meet, week, 'week3')
#     meet, week = check_meet(device, prob4, meet, week, 'week4')
#     meet, week = check_meet(device, prob5, meet, week, 'week5')
#     meet, week = check_meet(device, prob6, meet, week, 'week6')
#     meet, week = check_meet(device, prob7, meet, week, 'week7')
#     meet, week = check_meet(device, prob8, meet, week, 'week8')
#     meet, week = check_meet(device, prob9, meet, week, 'week9')
#     meet, week = check_meet(device, prob10, meet, week, 'week10')
#
# print meet_devices
#
# prob_file = file('probability/prob_file.csv', 'wb')
# writer = csv.writer(prob_file)
#
# week_file1 = file('probability/week_file1.csv', 'wb')
# week_file2 = file('probability/week_file2.csv', 'wb')
# week_file3 = file('probability/week_file3.csv', 'wb')
# week_file4 = file('probability/week_file4.csv', 'wb')
# week_file5 = file('probability/week_file5.csv', 'wb')
# week_file6 = file('probability/week_file6.csv', 'wb')
# week_file7 = file('probability/week_file7.csv', 'wb')
# week_file8 = file('probability/week_file8.csv', 'wb')
# week_file9 = file('probability/week_file9.csv', 'wb')
# week_file10 = file('probability/week_file10.csv', 'wb')
#
# writer1 = csv.writer(week_file1)
# writer2 = csv.writer(week_file2)
# writer3 = csv.writer(week_file3)
# writer4 = csv.writer(week_file4)
# writer5 = csv.writer(week_file5)
# writer6 = csv.writer(week_file6)
# writer7 = csv.writer(week_file7)
# writer8 = csv.writer(week_file8)
# writer9 = csv.writer(week_file9)
# writer10 = csv.writer(week_file10)
#
# yue_file8 = file('probability/yue_file8.csv', 'wb')
# yue_file9 = file('probability/yue_file9.csv', 'wb')
# writer8y = csv.writer(yue_file8)
# writer9y = csv.writer(yue_file9)
#
# for d in meet_devices:
#     # 月数据
#     if d in yue8:
#         writer8y.writerow(yue8[d])
#     if d in yue9:
#         writer9y.writerow(yue9[d])
#
#     # 周数据
#     l = []
#     l.append(str(d))
#
#     if d in zhou1:
#         l.append(zhou1[d][9])
#         writer1.writerow(zhou1[d])
#     else:
#         l.append('')
#
#     if d in zhou2:
#         l.append(zhou2[d][9])
#         writer2.writerow(zhou2[d])
#     else:
#         l.append('')
#
#     if d in zhou3:
#         l.append(zhou3[d][9])
#         writer3.writerow(zhou3[d])
#     else:
#         l.append('')
#
#     if d in zhou4:
#         l.append(zhou4[d][9])
#         writer4.writerow(zhou4[d])
#     else:
#         l.append('')
#
#     if d in zhou5:
#         l.append(zhou5[d][9])
#         writer5.writerow(zhou5[d])
#     else:
#         l.append('')
#
#     if d in zhou6:
#         l.append(zhou6[d][9])
#         writer6.writerow(zhou6[d])
#     else:
#         l.append('')
#
#     if d in zhou7:
#         l.append(zhou7[d][9])
#         writer7.writerow(zhou7[d])
#     else:
#         l.append('')
#
#     if d in zhou8:
#         l.append(zhou8[d][9])
#         writer8.writerow(zhou8[d])
#     else:
#         l.append('')
#
#     if d in zhou9:
#         l.append(zhou9[d][9])
#         writer9.writerow(zhou9[d])
#     else:
#         l.append('')
#
#     if d in zhou10:
#         l.append(zhou10[d][9])
#         writer10.writerow(zhou10[d])
#     else:
#         l.append('')
#
#     writer.writerow(l)
# do_search('yue8.csv', 'ret_yue8.csv')
# do_search('yue9.csv', 'ret_yue9.csv')
# do_search('zhou1.csv', 'ret_zhou1.csv')
# do_search('zhou2.csv', 'ret_zhou2.csv')
# do_search('zhou3.csv', 'ret_zhou3.csv')
# do_search('zhou4.csv', 'ret_zhou4.csv')
# do_search('zhou5.csv', 'ret_zhou5.csv')
# do_search('zhou6.csv', 'ret_zhou6.csv')
# do_search('zhou7.csv', 'ret_zhou7.csv')
# do_search('zhou8.csv', 'ret_zhou8.csv')
# do_search('zhou9.csv', 'ret_zhou9.csv')
# do_search('zhou10.csv', 'ret_zhou10.csv')

