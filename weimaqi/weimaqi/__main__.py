# coding=utf-8
import json

import datetime
from scrapy import cmdline


def getYesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    return yesterday

# TODO 分进程并行执行爬取任务
with open("../account.json") as account_file:
    load_account = json.load(account_file)
    yesterday = str(getYesterday())
    cmdline.execute(('scrapy crawl weimaqi -a uid='
                     + str(load_account[0]['uid'])
                     + ' -a pwd='
                     + str(load_account[0]['pwd'])
                     + ' -a yestoday='
                     + yesterday
                     + ' -a price=12'
                     + ' -o '
                     + str(load_account[0]['output'])
                     + '_' + yesterday
                     + '.csv').split())

    cmdline.execute(('scrapy crawl weimaqi -a uid='
                    + str(load_account[1]['uid'])
                    + ' -a pwd='
                    + str(load_account[1]['pwd'])
                    + ' -a yestoday='
                    + yesterday
                    + ' -a price=12'
                    + ' -o '
                    + str(load_account[1]['output'])
                    + '_' + yesterday
                    + '.csv').split())

    cmdline.execute(('scrapy crawl weimaqi -a uid='
                    + str(load_account[2]['uid'])
                    + ' -a pwd='
                    + str(load_account[2]['pwd'])
                    + ' -a yestoday='
                    + yesterday
                    + ' -a price=12'
                    + ' -o '
                    + str(load_account[2]['output'])
                    + '_' + yesterday
                    + '.csv').split())

    account_file.close()
