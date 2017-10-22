# coding=utf-8
import json

import time
from multiprocessing import Process

from scrapy import cmdline


class SpiderProcess(Process):
    def __init__(self, cmd):
        Process.__init__(self)
        self.cmd = cmd

    def run(self):
        print 'setting spider process execute'
        cmdline.execute(self.cmd)


if __name__ == '__main__':
    cmds = []
    # 是否全量拉取
    full = False
    with open("../account.json") as account_file:
        load_account = json.load(account_file)
        now = time.strftime("%Y-%m-%d[%H-%M-%S]", time.localtime())
        for i in range(0, len(load_account)):
            cmds.append(('scrapy crawl setting -a uid='
                         + str(load_account[i]['uid'])
                         + ' -a pwd='
                         + str(load_account[i]['pwd'])
                         + ' -a ch='
                         + str(load_account[i]['place'])
                         + ' -a full='
                         + str(full)
                         + ' -o '
                         + 'setting/setting' + '_' + now + '_' + str(load_account[i]['place'])
                         + '.csv').split())
        account_file.close()
    for c in cmds:
        p = SpiderProcess(c)
        p.daemon = True
        p.start()
        p.join()

    print 'setting spider execute finish'
