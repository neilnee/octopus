import json

import datetime
from scrapy import cmdline


def getyesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    return today - oneday


with open("../account.json") as account_file:
    load_account = json.load(account_file)
    yesterday = str(getyesterday())
    cmdline.execute(('scrapy crawl setting -a uid='
                     + str(load_account[2]['uid'])
                     + ' -a pwd='
                     + str(load_account[2]['pwd'])
                     + ' -o '
                     + 'setting/setting' + '_' + yesterday + '_' + str(load_account[2]['place'])
                     + '.csv').split())
    account_file.close()
