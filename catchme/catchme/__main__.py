# coding=utf-8
import calendar
import csv
import hashlib
import json
import time

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


class IncludeChannel:
    ch_code = ''
    ch_key = ''
    places = []
    revenue = {}
    revenue_wmq = []
    cpt = 2
    revenue_cvt = {}
    ret = 0
    name = ''
    with_wmq = True

    def __init__(self, channel_info, ysd):
        self.ch_code = channel_info['code']
        self.ch_key = md5(channel_info['name'])
        self.cpt = int(ch['cpt'])
        self.places = []
        self.revenue = {}
        self.revenue_wmq = []
        self.revenue_cvt = {}
        self.ret = float(channel_info['ret'])
        self.name = channel_info['name']
        struct_t = time.strptime(ysd, '%Y-%m-%d')
        self.ret = self.ret / calendar.monthrange(struct_t.tm_year, struct_t.tm_mon)[1]
        self.with_wmq = bool(channel_info['wmq'])

        if len(channel_info['include']) > 0:
            for place in channel_info['include']:
                if time.strptime(ysd, '%Y-%m-%d') >= time.strptime(place['start'], '%Y-%m-%d'):
                    place_key = md5(place['name'])
                    self.places.append(place_key)
                    self.revenue[place_key] = [0] * 12
                    self.revenue[place_key][0] = str(place['name'].encode('utf-8'))
                    self.revenue[place_key][11] = int(place['disable'])
                    if place['start'] == ysd:
                        self.revenue[place_key][1] = -float(place['test_income'])
                        self.revenue[place_key][3] = -float(place['test_income']) + float(place['test_cost'])
                        self.revenue[place_key][6] = -float(place['test_gift'])
                        self.revenue[place_key][9] = -float(place['test_play'])
                        self.revenue[place_key][7] = -int(place['test_play'] * self.cpt)
                    ori_key = md5(place['original'])
                    self.revenue_cvt[ori_key] = place_key

    def append_weimaqi_data(self, input_line):
        ori_key = md5(input_line[0], False)
        if ori_key in self.revenue_cvt.keys() and self.revenue_cvt[ori_key] in self.revenue.keys():
            revenue_line = self.revenue[self.revenue_cvt[ori_key]]
            revenue_line[1] += float(input_line[1])
            revenue_line[3] += float(input_line[3])
            revenue_line[6] += int(input_line[6])
            revenue_line[9] += int(input_line[9])
            revenue_line[7] += int(input_line[7]) * self.cpt
            revenue_line[8] += int(input_line[8])
            # noinspection PyBroadException
            try:
                revenue_line[5] = float(revenue_line[6]) / float(revenue_line[9])
            except Exception:
                revenue_line[5] = 0.0
            if int(revenue_line[10]) == 0 and int(revenue_line[11]) == 0:
                revenue_line[10] = int(input_line[10])
                revenue_line[11] = int(input_line[11])
            revenue_line[2] = float(revenue_line[1]) / (revenue_line[10] + revenue_line[11])
            revenue_line[4] = revenue_line[3] / (revenue_line[10] + revenue_line[11])
        else:
            self.revenue_wmq.append(input_line)

    def append_catchme_data(self, input_line):
        place_key = md5(str(input_line[2]).strip(), False)
        if place_key in self.revenue.keys():
            revenue_line = self.revenue[place_key]
            revenue_line[1] += float(input_line[6])
            revenue_line[3] += float(input_line[6]) - float(input_line[9])
            revenue_line[6] += int(input_line[8])
            revenue_line[9] += int(input_line[7])
            revenue_line[7] += int(input_line[7]) * self.cpt
            revenue_line[8] = 0
            # noinspection PyBroadException
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

    def calculat_total_revenue(self):
        income = 0.0
        income_ave = 0.0
        profit = 0.0
        profit_ave = 0.0
        profit_net = 0.0
        profit_net_ave = 0.0
        profit_net_percent = 0.0
        probability = 0.0
        total_device = 0
        total_place = 0

        total_play = 0
        total_gift = 0

        if len(self.revenue) > 0:
            for place in self.revenue.values():
                income += float(place[1])
                profit += float(place[3])
                total_device += int(place[10]) + int(place[11])
                total_place += 1
                total_play += int(place[9])
                total_gift += int(place[6])
        if len(self.revenue_wmq) > 0:
            for place in self.revenue_wmq:
                income += float(place[1])
                profit += float(place[3])
                total_device += int(place[10]) + int(place[11])
                total_place += 1
                total_play += int(place[9])
                total_gift += int(place[6])
        income_ave = income / total_device
        profit_ave = profit / total_device
        profit_net = profit - self.ret
        profit_net_ave = profit_net / total_device
        profit_net_percent = profit_net / income
        probability = float(total_gift) / float(total_play)

        return self.name.encode('utf-8'), income, income_ave, profit, profit_ave, profit_net, profit_net_ave, \
               profit_net_percent, probability, total_device, total_place, total_play, total_gift


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
        idx = 0
        for li in wmq_file:
            idx = idx + 1
            if idx == 1:
                continue
            li = li.strip()
            li = li.replace('\r\n', '')
            li_list = li.split(',')
            ch_item.append_weimaqi_data(li_list)


if __name__ == '__main__':
    yesterday = str(getyesterday())

    with open("../channel.json") as ch_file:
        load_ch = json.load(ch_file)
        for ch in load_ch:
            if ch['name']:
                includes[md5(ch['name'])] = IncludeChannel(ch, yesterday)

    cmds = []
    with open("../account.json") as account_file:
        load_account = json.load(account_file)
        for i in range(0, len(load_account)):
            cmds.append(('scrapy crawl weimaqi -a uid='
                         + str(load_account[i]['uid'])
                         + ' -a pwd='
                         + str(load_account[i]['pwd'])
                         + ' -a yesterday='
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
                p_key = md5(str(line_list[2]).strip(), False)
                if p_key in includes[c_key].places:
                    includes[c_key].append_catchme_data(line_list)

    t_income = 0.0
    t_income_ave = 0.0
    t_profit = 0.0
    t_profit_ave = 0.0
    t_profit_net = 0.0
    t_profit_net_ave = 0.0
    t_profit_net_percent = 0.0
    t_probability = 0.0
    t_total_device = 0
    t_total_place = 0

    t_total_play = 0
    t_total_gift = 0

    place_output = []

    writer = csv.writer(file('revenue/revenue_' + yesterday + '.csv', 'wb'))
    for item in includes.values():
        if item.with_wmq:
            load_weimaqi('revenue/weimaqi/revenue_' + yesterday + '_' + item.ch_code + '.csv',
                         includes[md5(item.name)])
        writer.writerows(item.revenue.values())
        if item.with_wmq:
            writer.writerows(item.revenue_wmq)
        writer.writerow('')
        out_name, out_income, out_income_ave, out_profit, out_profit_ave, out_profit_net, out_profit_net_ave, \
        out_profit_net_percent, out_probability, out_total_device, out_total_place, out_play, out_gift \
            = item.calculat_total_revenue()

        t_income += out_income
        t_profit += out_profit
        t_profit_net += out_profit_net
        t_total_device += out_total_device
        t_total_place += out_total_place
        t_total_play += out_play
        t_total_gift += out_gift
        t_income_ave = t_income / t_total_device
        t_profit_ave = t_profit / t_total_device
        t_profit_net_ave = t_profit_net / t_total_device
        t_profit_net_percent = t_profit_net / t_income
        t_probability = float(t_total_gift) / float(t_total_play)

        place_output.append('\n[渠道数据 - ' + out_name
                            + ']\n营收: ' + str(round(out_income, 1))
                            + '\n台均营收: ' + str(round(out_income_ave, 1))
                            + '\n去娃娃盈利: ' + str(round(out_profit, 1))
                            + '\n去娃娃台均盈利: ' + str(round(out_profit_ave, 1))
                            + '\n去租金去娃娃盈利: ' + str(round(out_profit_net, 1))
                            + '\n去租金去娃娃台均盈利: ' + str(round(out_profit_net_ave, 1))
                            + '\n去租金去娃娃盈利率: ' + str(round(out_profit_net_percent * 100, 2))
                            + '%\n抓取概率: ' + str(round(out_probability * 100, 2))
                            + '%\n总台数: ' + str(out_total_device)
                            + '\n总场地数: ' + str(out_total_place))

    time.sleep(3)

    print ('\n[汇总数据]'
           + '\n营收: ' + str(round(t_income, 1))
           + '\n台均营收: ' + str(round(t_income_ave, 1))
           + '\n去娃娃盈利: ' + str(round(t_profit, 1))
           + '\n去娃娃台均盈利: ' + str(round(t_profit_ave, 1))
           + '\n去租金去娃娃盈利: ' + str(round(t_profit_net, 1))
           + '\n去租金去娃娃台均盈利: ' + str(round(t_profit_net_ave, 1))
           + '\n去租金去娃娃盈利率: ' + str(round(t_profit_net_percent * 100, 2))
           + '%\n抓取概率: ' + str(round(t_probability * 100, 2))
           + '%\n总台数: ' + str(t_total_device)
           + '\n总场地数: ' + str(t_total_place))

    for output_line in place_output:
        print (output_line)
