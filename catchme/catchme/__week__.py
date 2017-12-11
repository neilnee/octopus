# coding=utf-8
import csv
import httplib
import json
import threading
import time

from multiprocessing import Process


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
    json_obj = json.loads(response.read())
    cinemas = json_obj['data1']
    t = json_obj['pCount']
    for i in range(0, len(cinemas)):
        ret.append(Cinema(cinemas[i]))
    conn.close()
    return ret, t


class CinemaProcess(Process):
    start_idx = 0
    end_idx = 0
    week_idx = 0

    def __init__(self, start, end, w_idx):
        Process.__init__(self)
        self.start_idx = start
        self.end_idx = end
        self.week_idx = w_idx

    def run(self):
        print('thread run : ' + str(self.start_idx) + " to " + str(self.end_idx))
        for idx in range(self.start_idx, self.end_idx + 1):
            cinema_list, t = request_cinema_data(idx, self.week_idx)
            append_cinema_list(cinema_list)
            if len(cinema_list) < 10:
                break
        global lockp
        global t_list
        lockp.acquire()
        t_list.remote(self)
        lockp.release()


def append_cinema_list(cinema_list):
    lock.acquire()
    global ids
    global count
    global writer
    for cinema in cinema_list:
        if cinema.cinemaId not in ids:
            ids.append(cinema.cinemaId)
            writer.writerow(cinema.output())
            count += 1
            print('影院[' + cinema.cinemaName + ']导入完成;总数[' + str(count) + ']')
    lock.release()


week_idx = 979
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


lock = threading.Lock()
lockp = threading.Lock()
ids = []
count = 0
index = 2
c_list, total = request_cinema_data(1, week_idx)
total = total - 1
append_cinema_list(c_list)
t_list = []

while total > 500:
    idx_s = index
    idx_e = index + 500
    total = total - 500
    index = idx_e + 1
    p = CinemaProcess(idx_s, idx_e, week_idx)
    t_list.append(p)
    p.daemon = True
    p.start()

if total > 0:
    p = CinemaProcess(index, index + total, week_idx)
    t_list.append(p)
    p.daemon = True
    p.start()


while True:
    lockp.acquire()
    if len(t_list) > 0:
        time.sleep(5)
    else:
        break
    lockp.release()
