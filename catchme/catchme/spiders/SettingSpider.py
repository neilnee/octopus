# coding=utf-8
import hashlib
import json
import random
import time
import re

import scrapy
from scrapy import Request, FormRequest, Selector
from scrapy.spiders import CrawlSpider

from ..items import SettingItem


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
    channel = ''
    full = True
    setting_map = {}

    def __init__(self, uid='', pwd='', ch='', full=True, *args, **kwargs):
        super(SettingSpider, self).__init__(*args, **kwargs)
        self.uid = uid
        self.pwd = pwd
        self.full = full
        with open("../account.json") as account_file:
            load_account = json.load(account_file)
            for i in range(0, len(load_account)):
                if load_account[i]['place'] == ch:
                    self.channel = load_account[i]['name']
                    break
        with open("setting/setting_current.csv") as setting_file:
            i = 0
            for line in setting_file:
                if i == 0:
                    i = i + 1
                    continue
                i = i + 1
                line = line.strip()
                line_d = line.split(',')
                item = SettingItem()
                item['channel'] = str(line_d[0])
                item['d_name'] = str(line_d[1])
                item['device_id'] = str(line_d[2])
                item['tag'] = str(line_d[3])
                item['des'] = str(line_d[4])
                item['online'] = str(line_d[5])
                item['setting_param'] = int(line_d[6])
                item['coin_per_time'] = int(line_d[7])
                item['game_duration'] = int(line_d[8])
                item['music'] = int(line_d[9])
                item['air_pick'] = int(line_d[10])
                item['out_pos'] = int(line_d[11])
                item['shake_clear'] = int(line_d[12])
                item['music_volume'] = int(line_d[13])
                item['free_for_continue'] = int(line_d[14])
                item['strong_force'] = int(line_d[15])
                item['weak_force'] = int(line_d[16])
                item['pick_height'] = int(line_d[17])
                item['strong_to_weak'] = int(line_d[18])
                item['line_height'] = int(line_d[19])
                item['out_mode'] = int(line_d[20])
                item['probability'] = int(line_d[21])
                item['eyes'] = int(line_d[22])
                item['keep'] = int(line_d[23])
                item['account_clear'] = int(line_d[24])
                item['reset'] = int(line_d[25])
                item['disable_btn'] = int(line_d[26])
                item['disable_board'] = int(line_d[27])
                self.setting_map[item['device_id']] = item
            print ('init finish: ' + str(len(self.setting_map)))

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

    # noinspection PyUnusedLocal
    def check_info(self, response):
        return [Request('https://weimaqi.net/admin_mchm_new/CheckInfo_m.aspx?r=' + str(random.random()),
                        callback=self.handle_check_info)]

    # noinspection PyUnusedLocal
    def handle_check_info(self, response):
        return [Request('https://weimaqi.net/admin_mchm_new/control/Handler.ashx?action=device_mngt&_='
                        + str(long(time.time()) * 1000l),
                        callback=self.handle_devices)]

    def handle_devices(self, response):
        setting_list = json.loads(re.search("\\'data\\':\\[.+", response.body).group()[7:-2])
        for i in range(0, len(setting_list)):
            item = None
            if self.full == 'False' and setting_list[i]['device_id'] in self.setting_map.keys():
                item = self.setting_map[setting_list[i]['device_id']]
            if item and item.is_valid():
                print ('1: found usable item')
                yield item
            else:
                if setting_list[i]['online'] == '1':
                    print ('1: get device setting: ' + setting_list[i]['d_name'])
                    yield scrapy.FormRequest(
                        'https://weimaqi.net/admin_mchm_new/control/shebeisettingsHandler.ashx?action=getdatasid_load',
                        method='POST',
                        formdata={
                            'id': setting_list[i]['device_id'],
                            'num0_1': '3',
                            'cid': '0',
                            'settingsid': '63'
                        },
                        meta={
                            'device_id': setting_list[i]['device_id'],
                            'd_name': setting_list[i]['d_name'],
                            'tag': setting_list[i]['tag'],
                            'des': setting_list[i]['des']
                        },
                        callback=self.handle_datasidload,
                        dont_filter=True)
                else:
                    print ('1: found unuseable device: ' + setting_list[i]['d_name'])
                    yield self.unuseable_device(setting_list[i]['device_id'],
                                                setting_list[i]['d_name'],
                                                setting_list[i]['tag'],
                                                setting_list[i]['des'])

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
                'device_id': response.meta['device_id'],
                'd_name': response.meta['d_name'],
                'tag': response.meta['tag'],
                'des': response.meta['des']
            },
            callback=self.handle_setting,
            dont_filter=True)]

    def handle_setting(self, response):
        data = json.loads(response.body)
        if len(data) > 0 and data[0]['result'] == 'ok':
            return [scrapy.Request(
                'https://weimaqi.net/admin_mchm_new/control/shebeisettingsHandler.ashx?action=getstate&sn='
                + data[0]['data'],
                method='GET',
                meta={
                    'receiveid': data[0]['receiveid'],
                    'device_id': response.meta['device_id'],
                    'd_name': response.meta['d_name'],
                    'tag': response.meta['tag'],
                    'des': response.meta['des']
                },
                callback=self.handle_state)]
        else:
            print ('2: found unuseable device: ' + response.meta['d_name'])
            return self.unuseable_device(response.meta['device_id'],
                                         response.meta['d_name'],
                                         response.meta['tag'],
                                         response.meta['des'])

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
                    'device_id': response.meta['device_id'],
                    'd_name': response.meta['d_name'],
                    'tag': response.meta['tag'],
                    'des': response.meta['des']
                },
                callback=self.handle_datas,
                dont_filter=True
            )]
        else:
            print ('3: found unuseable device: ' + response.meta['d_name'])
            return self.unuseable_device(response.meta['device_id'],
                                         response.meta['d_name'],
                                         response.meta['tag'],
                                         response.meta['des'])

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
                    'device_id': response.meta['device_id'],
                    'd_name': response.meta['d_name'],
                    'tag': response.meta['tag'],
                    'des': response.meta['des']
                },
                callback=self.handle_receivedata,
                dont_filter=True
            )]
        else:
            print ('4: found unuseable device: ' + response.meta['d_name'])
            return self.unuseable_device(response.meta['device_id'],
                                         response.meta['d_name'],
                                         response.meta['tag'],
                                         response.meta['des'])

    # noinspection PyMethodMayBeStatic,PyBroadException
    def handle_receivedata(self, response):
        item = SettingItem()
        item['channel'] = self.channel
        item['device_id'] = response.meta['device_id']
        item['d_name'] = response.meta['d_name']
        item['tag'] = response.meta['tag']
        item['des'] = response.meta['des']
        item['online'] = '在线'
        try:
            item['setting_param'] = int(Selector(text=response.body).xpath('//*[@id="num0_1"]/@value')[0].extract())
        except Exception:
            item['setting_param'] = -1

        try:
            item['coin_per_time'] = int(Selector(text=response.body).xpath('//*[@id="num1_1"]/@value')[0].extract())
        except Exception:
            item['coin_per_time'] = -1

        try:
            item['game_duration'] = int(Selector(text=response.body).xpath('//*[@id="num2_1"]/@value')[0].extract())
        except Exception:
            item['game_duration'] = -1

        try:
            item['music'] = int(Selector(text=response.body).xpath('//*[@id="num3_1"]/@value')[0].extract())
        except Exception:
            item['music'] = -1

        try:
            item['air_pick'] = int(Selector(text=response.body).xpath('//*[@id="num4_1"]/@value')[0].extract())
        except Exception:
            item['air_pick'] = -1

        try:
            item['out_pos'] = int(Selector(text=response.body).xpath('//*[@id="num5_1"]/@value')[0].extract())
        except Exception:
            item['out_pos'] = -1

        try:
            item['shake_clear'] = int(Selector(text=response.body).xpath('//*[@id="num6_1"]/@value')[0].extract())
        except Exception:
            item['shake_clear'] = -1

        try:
            item['music_volume'] = int(Selector(text=response.body).xpath('//*[@id="num7_1"]/@value')[0].extract())
        except Exception:
            item['music_volume'] = -1

        try:
            item['free_for_continue'] = int(Selector(text=response.body).xpath('//*[@id="num8_1"]/@value')[0].extract())
        except Exception:
            item['free_for_continue'] = -1

        try:
            item['strong_force'] = int(Selector(text=response.body).xpath('//*[@id="num9_1"]/@value')[0].extract())
        except Exception:
            item['strong_force'] = -1

        try:
            item['weak_force'] = int(Selector(text=response.body).xpath('//*[@id="num10_1"]/@value')[0].extract())
        except Exception:
            item['weak_force'] = -1

        try:
            item['pick_height'] = int(Selector(text=response.body).xpath('//*[@id="num11_1"]/@value')[0].extract())
        except Exception:
            item['pick_height'] = -1

        try:
            item['strong_to_weak'] = int(Selector(text=response.body).xpath('//*[@id="num12_1"]/@value')[0].extract())
        except Exception:
            item['strong_to_weak'] = -1

        try:
            item['line_height'] = int(Selector(text=response.body).xpath('//*[@id="num13_1"]/@value')[0].extract())
        except Exception:
            item['line_height'] = -1

        try:
            item['out_mode'] = int(Selector(text=response.body).xpath('//*[@id="num14_1"]/@value')[0].extract())
        except Exception:
            item['out_mode'] = -1

        try:
            item['probability'] = int(Selector(text=response.body).xpath('//*[@id="num15_1"]/@value')[0].extract())
        except Exception:
            item['probability'] = -1

        try:
            item['eyes'] = int(Selector(text=response.body).xpath('//*[@id="num16_1"]/@value')[0].extract())
        except Exception:
            item['eyes'] = -1

        try:
            item['keep'] = int(Selector(text=response.body).xpath('//*[@id="num17_1"]/@value')[0].extract())
        except Exception:
            item['keep'] = -1

        try:
            item['account_clear'] = int(Selector(text=response.body).xpath('//*[@id="num18_1"]/@value')[0].extract())
        except Exception:
            item['account_clear'] = -1

        try:
            item['reset'] = int(Selector(text=response.body).xpath('//*[@id="num19_1"]/@value')[0].extract())
        except Exception:
            item['reset'] = -1

        try:
            item['disable_btn'] = int(Selector(text=response.body).xpath('//*[@id="num20_1"]/@value')[0].extract())
        except Exception:
            item['disable_btn'] = -1

        try:
            item['disable_board'] = int(Selector(text=response.body).xpath('//*[@id="num21_1"]/@value')[0].extract())
        except Exception:
            item['disable_board'] = -1

        yield item

    # noinspection PyMethodMayBeStatic
    def unuseable_device(self, device_id='', d_name='', tag='', des=''):
        item = SettingItem()
        item['channel'] = self.channel
        item['d_name'] = d_name
        item['device_id'] = device_id
        item['tag'] = tag
        item['des'] = des
        item['online'] = '离线'
        item['setting_param'] = -1
        item['coin_per_time'] = -1
        item['game_duration'] = -1
        item['music'] = -1
        item['air_pick'] = -1
        item['out_pos'] = -1
        item['shake_clear'] = -1
        item['music_volume'] = -1
        item['free_for_continue'] = -1
        item['strong_force'] = -1
        item['weak_force'] = -1
        item['pick_height'] = -1
        item['strong_to_weak'] = -1
        item['line_height'] = -1
        item['out_mode'] = -1
        item['probability'] = -1
        item['eyes'] = -1
        item['keep'] = -1
        item['account_clear'] = -1
        item['reset'] = -1
        item['disable_btn'] = -1
        item['disable_board'] = -1
        return item
