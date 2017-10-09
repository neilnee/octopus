import hashlib
import json
import random
import time
import re

import scrapy
from scrapy import Request, FormRequest
from scrapy.spiders import CrawlSpider


class SettingSpider(CrawlSpider):
    name = 'setting'
    allowed_domains = ['weimaqi.net']
    start_urls = ['https://weimaqi.net/admin_mchm_new/login.html']
    headers = {
        "Accept": "*/*",
        "Accept - Encoding": "gzip, deflate, br",
        "Accept - Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": 37,
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "weimaqi.net",
        "Origin": "https://weimaqi.net",
        "Pragma": "no-cache",
        "Referer": "https://weimaqi.net/admin_mch_new/login.aspx",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/60.0.3112.113 Mobile Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    uid = ''
    pwd = ''

    def __init__(self, uid='', pwd='', *args, **kwargs):
        super(SettingSpider, self).__init__(*args, **kwargs)
        self.uid = uid
        self.pwd = pwd

    def start_requests(self):
        return [Request("https://weimaqi.net/admin_mchm_new/login.html",
                        callback=self.start_login)]

    def start_login(self, response):
        return [FormRequest.from_response(response,
                                          url='https://weimaqi.net/admin_mchm_new/control/Handler.ashx?action=login',
                                          method='POST',
                                          formdata={
                                              'mch_acc': self.uid,
                                              'mch_pwd': hashlib.md5(
                                                  hashlib.md5(self.pwd).hexdigest().upper()).hexdigest(),
                                              'auto': 'false'},
                                          callback=self.check_info,
                                          dont_filter=True)]

    def check_info(self, response):
        return [Request('https://weimaqi.net/admin_mchm_new/CheckInfo_m.aspx?r=' + str(random.random()),
                        callback=self.handle_check_info)]

    def handle_check_info(self, response):
        return [Request('https://weimaqi.net/admin_mchm_new/control/Handler.ashx?action=device_mngt&_='
                        + str(long(time.time()) * 1000l),
                        callback=self.handle_devices)]

    # noinspection PyMethodMayBeStatic
    def handle_devices(self, response):
        setting_list = json.loads(re.search("\\'data\\':\\[.+", response.body).group()[7:-2])
        for i in range(0, len(setting_list)):
            print (setting_list[i]['device_id'] + ';' + setting_list[i]['d_name'])
            if setting_list[i]['online'] == '1':
                yield scrapy.FormRequest(
                    'https://weimaqi.net/admin_mchm_new/control/shebeisettingsHandler.ashx?action=getdatasid_load',
                    method='POST',
                    formdata={
                        'id': setting_list[i]['device_id'],
                        'num0_1': '3',
                        'cid': '0',
                        'settingsid': '63'
                    },
                    meta={'device_id': setting_list[i]['device_id']},
                    callback=self.handle_datasidload,
                    dont_filter=True)

    def handle_datasidload(self, response):
        return [scrapy.FormRequest(
            'https://weimaqi.net/admin_mchm_new/control/shebeisettingsHandler.ashx?action=settings',
            method='POST',
            formdata={
                'id': response.meta['device_id'],
                'num0_1': '3',
                'cid': '0',
                'settingsid': '63'
            },
            meta={
                'device_id': response.meta['device_id']
            },
            callback=self.handle_setting,
            dont_filter=True)]
        pass

    def handle_setting(self, response):
        data = json.loads(response.body)
        if len(data) > 0 and data[0]['result'] == 'ok':
            return [scrapy.Request(
                'https://weimaqi.net/admin_mchm_new/control/shebeisettingsHandler.ashx?action=getstate&sn='
                + data[0]['data'],
                method='GET',
                meta={
                    'receiveid': data[0]['receiveid'],
                    'device_id': response.meta['device_id']
                },
                callback=self.handle_state)]

    def handle_state(self, response):
        data = json.loads(response.body)
        if len(data) > 0 and data[0]['result'] == 'ok':
            return [scrapy.FormRequest(
                'https://weimaqi.net/admin_mchm_new/control/shebeisettingsHandler.ashx?action=getdatas',
                method='POST',
                formdata={
                    'receiveid': response.meta['receiveid'],
                    'did': response.meta['device_id'],
                    'cid': '0',
                    'settingsid': '63'
                },
                meta={
                    'device_id': response.meta['device_id']
                },
                callback=self.handle_datas,
                dont_filter=True
            )]

    def handle_datas(self, response):
        sn = re.search("GetDataed\\('.+',", response.body).group()[11:-2]
        if sn:
            return [scrapy.FormRequest(
                'https://weimaqi.net/admin_mchm_new/control/shebeisettingsHandler.ashx?action=getrecivedata',
                method='POST',
                formdata={
                    'h_sn': sn,
                    'h_tid': '63'
                },
                meta={
                    'device_id': response.meta['device_id']
                },
                callback=self.handle_receivedata,
                dont_filter=True
            )]

    def handle_receivedata(self, response):
        print (response.body)
