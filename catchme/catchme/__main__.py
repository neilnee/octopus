# coding=utf-8
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
    name = ''
    channels = []

    def __init__(self, name, channels):
        self.name = name
        self.channels = channels

# 加载catchme数据时需要包含的渠道场地
includes = []


def md5(input_str):
    return hashlib.md5(input_str.encode('utf-meetdevice8')).hexdigest()


def getyesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    return today - oneday

if __name__ == '__main__':
    with open("../channel.json") as ch_file:
        load_ch = json.load(ch_file)
        for ch in load_ch:
            n = md5(ch['name'])
            c = []
            if len(ch['include']) > 0:
                for i in ch['include']:
                    c.append(md5(i))
            includes.append(InCludeChannel(n, c))

    # cmds = []
    # with open("../account.json") as account_file:
    #     load_account = json.load(account_file)
    #     yesterday = str(getyesterday())
    #     for i in range(0, len(load_account)):
    #         cmds.append(('scrapy crawl weimaqi -a uid='
    #                     + str(load_account[i]['uid'])
    #                     + ' -a pwd='
    #                     + str(load_account[i]['pwd'])
    #                     + ' -a yestoday='
    #                     + yesterday
    #                     + ' -a price=12'
    #                     + ' -a ch='
    #                     + str(load_account[i]['place'])
    #                     + ' -a cpt='
    #                     + str(load_account[i]['cpt'])
    #                     + ' -o '
    #                     + 'revenue/weimaqi/revenue' + '_' + yesterday + '_' + str(load_account[i]['place'])
    #                     + '.csv').split())
    #     account_file.close()
    # for c in cmds:
    #     p = SpiderProcess(c)
    #     p.daemon = True
    #     p.start()
    #     p.join()



    print 'main spider execute finish'
