# coding=utf-8
import csv
import httplib
import json


class Cinema:
    cinemaId = ''  # 影院ID
    cinemaName = ''  # 影院名称
    amount = 0.0  # 当周票房
    scenes = 0.0  # 当周场次
    avgScreen = 0.0  # 单荧幕平均周票房
    avgPS = 0.0  # 场均人次
    screen_yield = 0.0  # 单日单厅票房
    scenes_time = 0.0  # 单日单厅场次

    def __init__(self, json_cinema):
        self.cinemaId = str(json_cinema['cinemaId'])
        self.cinemaName = str(json_cinema['cinemaName'].encode('utf-8'))
        self.amount = float(json_cinema['amount'])
        self.scenes = float(json_cinema['scenes'])
        self.avgScreen = float(json_cinema['avgScreen'])
        self.avgPS = float(json_cinema['avgPS'])
        self.screen_yield = float(json_cinema['screen_yield'])
        self.scenes_time = float(json_cinema['scenes_time'])

    def output(self):
        output = [0] * 8
        output[0] = self.cinemaId
        output[1] = self.cinemaName
        output[2] = self.amount
        output[3] = self.scenes
        output[4] = self.avgScreen
        output[5] = self.avgPS
        output[6] = self.screen_yield
        output[7] = self.scenes_time
        return output


def request_cinema_data(idx, week):
    ret = []
    conn = httplib.HTTPConnection("www.cbooo.cn")
    conn.request("GET", "/BoxOffice/getCBW?pIndex=" + str(idx) + "&dt=" + str(week))
    response = conn.getresponse()
    # print "request response : " + str(response.status)
    cinemas = json.loads(response.read())['data1']
    for i in range(0, len(cinemas)):
        ret.append(Cinema(cinemas[i]))
    conn.close()
    return ret


week_idx = 978
writer = csv.writer(file('week/cbooo/week_' + str(week_idx) + '.csv', 'wb'))
title = [0] * 8
title[0] = '影院ID'
title[1] = '影院名称'
title[2] = '当周票房'
title[3] = '当周场次'
title[4] = '单荧幕平均周票房'
title[5] = '场均人次'
title[6] = '单日单厅票房'
title[7] = '单日单厅场次'
writer.writerow(title)
index = 1
count = 0
ids = []
while index > 0:
    cinema_list = request_cinema_data(index, week_idx)
    for cinema in cinema_list:
        if cinema.cinemaId not in ids:
            ids.append(cinema.cinemaId)
            writer.writerow(cinema.output())
            count += 1
            print('影院[' + cinema.cinemaName + ']导入完成;总数[' + str(count) + ']')
    if len(cinema_list) >= 10:
        index += 1
    else:
        index = -1
