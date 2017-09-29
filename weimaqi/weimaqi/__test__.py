# coding=utf-8
import hashlib
import json

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

print hashlib.md5(hashlib.md5("catchme@5107yl").hexdigest().upper()).hexdigest()
