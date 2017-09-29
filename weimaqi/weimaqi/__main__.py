# coding=utf-8
import json

import datetime
from multiprocessing import Process

from scrapy import cmdline


def getyesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    return today - oneday


class SpiderProcess(Process):
    def __init__(self, cmd):
        Process.__init__(self)
        self.cmd = cmd

    def run(self):
        print 'process execute'
        cmdline.execute(self.cmd)


if __name__ == '__main__':
    cmds = []
    with open("../account.json") as account_file:
        load_account = json.load(account_file)
        yesterday = str(getyesterday())
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
                        + str(load_account[i]['output'])
                        + '_' + yesterday
                        + '.csv').split())
        account_file.close()
    for c in cmds:
        p = SpiderProcess(c)
        p.daemon = True
        p.start()
        p.join()

    print 'spider execute finish'
