# coding=utf-8
import csv
import hashlib
import json

import datetime
from multiprocessing import Process

from scrapy import cmdline


class SpiderProcess(Process):
    def __init__(self, cmd):
        Process.__init__(self)
        self.cmd = cmd

    def run(self):
        print 'main spider process execute'
        cmdline.execute(self.cmd)


class InCludeChannel:
    ch_code = ''
    ch_key = ''
    channels = []
    revenue = {}
    revenue_wmq = []
    cpt = 2

    def __init__(self, ch_code, ch_key, channels, cpt=2):
        self.ch_code = ch_code
        self.ch_key = ch_key
        self.channels = channels
        self.revenue = {}
        self.cpt = cpt
        self.revenue_wmq = []

    def append_weimaqi_data(self, input_line):
        self.revenue_wmq.append(input_line)

    def append_catchme_data(self, input_line):
        place_key = md5(input_line[2], False)
        if place_key in self.revenue.keys():
            revenue_line = self.revenue[place_key]
            revenue_line[1] += float(input_line[6])
            revenue_line[3] += float(input_line[6]) - float(input_line[9])
            revenue_line[6] += int(input_line[8])
            revenue_line[7] += int(input_line[7]) / self.cpt
            revenue_line[8] = 0
            revenue_line[9] += int(input_line[7])
            try:
                revenue_line[5] = float(revenue_line[6]) / float(revenue_line[9])
            except Exception:
                revenue_line[5] = 0.0
            if input_line[12]:
                revenue_line[10] += 1
            else:
                revenue_line[11] += 1
            revenue_line[2] = float(revenue_line[1]) / (revenue_line[10] + revenue_line[11])
            revenue_line[4] = revenue_line[3] / (revenue_line[10] + revenue_line[11])
        else:
            revenue_line = [0] * 12
            revenue_line[0] = str(input_line[2])
            revenue_line[1] = float(input_line[6])
            revenue_line[3] = float(input_line[6]) - float(input_line[9])
            try:
                revenue_line[5] = float(input_line[8]) / float(input_line[7])
            except Exception:
                revenue_line[5] = 0.0
            revenue_line[6] = int(input_line[8])
            revenue_line[7] = int(input_line[7]) / self.cpt
            revenue_line[8] = 0
            revenue_line[9] = int(input_line[7])
            if input_line[12]:
                revenue_line[10] = 1
            else:
                revenue_line[11] = 1
            revenue_line[2] = float(input_line[6]) / (revenue_line[10] + revenue_line[11])
            revenue_line[4] = revenue_line[3] / (revenue_line[10] + revenue_line[11])
            self.revenue[place_key] = revenue_line


# 加载catchme数据时需要包含的渠道场地
includes = {}


def md5(input_str, encode=True):
    if encode:
        return hashlib.md5(input_str.encode('utf-8')).hexdigest()
    else:
        return hashlib.md5(input_str).hexdigest()


def getyesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    return today - oneday


def load_weimaqi(input_file, ch_item):
    with open(input_file) as wmq_file:
        i = 0
        for l in wmq_file:
            i = i + 1
            if i == 1:
                continue
            l = l.strip()
            l = l.replace('\r\n', '')
            l_list = l.split(',')
            ch_item.append_weimaqi_data(l_list)

if __name__ == '__main__':
    yesterday = str(getyesterday())

    with open("../channel.json") as ch_file:
        load_ch = json.load(ch_file)
        for ch in load_ch:
            c_key = md5(ch['name'])
            place = []
            if len(ch['include']) > 0:
                for i in ch['include']:
                    place.append(md5(i))
            includes[c_key] = InCludeChannel(ch['code'], c_key, place, int(ch['cpt']))

    cmds = []
    with open("../account.json") as account_file:
        load_account = json.load(account_file)
        for i in range(0, len(load_account)):
            cmds.append(('scrapy crawl weimaqi -a uid='
                        + str(load_account[i]['uid'])
                        + ' -a pwd='
                        + str(load_account[i]['pwd'])
                        + ' -a yestoday='
                        + yesterday
                        + ' -a price=12'
                        + ' -a ch='
                        + str(load_account[i]['place'])
                        + ' -a cpt='
                        + str(load_account[i]['cpt'])
                        + ' -o '
                        + 'revenue/weimaqi/revenue' + '_' + yesterday + '_' + str(load_account[i]['place'])
                        + '.csv').split())
        account_file.close()
    for c in cmds:
        p = SpiderProcess(c)
        p.daemon = True
        p.start()
        p.join()

    with open('revenue/catchme/revenue_' + yesterday + '_c.csv') as catchme_file:
        for line in catchme_file:
            line = line.strip()
            line = line.replace('\r\n', '')
            line_list = line.split(',')
            c_key = md5(line_list[1], False)
            if c_key in includes.keys():
                p_key = md5(line_list[2], False)
                if p_key in includes[c_key].channels:
                    includes[c_key].append_catchme_data(line_list)

    load_weimaqi('revenue/weimaqi/revenue_' + yesterday + '_yl.csv', includes[md5('耀莱', False)])
    load_weimaqi('revenue/weimaqi/revenue_' + yesterday + '_hd.csv', includes[md5('恒大', False)])
    load_weimaqi('revenue/weimaqi/revenue_' + yesterday + '_xh.csv', includes[md5('星河', False)])

    writer = csv.writer(file('revenue/revenue_' + yesterday + '.csv', 'wb'))
    for item in includes.values():
        writer.writerows(item.revenue.values())
        writer.writerows(item.revenue_wmq)
        writer.writerow('')

    print 'main spider execute finish'
