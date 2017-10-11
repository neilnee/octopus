# coding=utf-8
import hashlib
import json
import random

import datetime
import time
from scrapy import cmdline

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

print (datetime)
