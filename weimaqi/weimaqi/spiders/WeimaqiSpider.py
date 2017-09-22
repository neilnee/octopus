# coding=utf-8
import json

import datetime, re, scrapy
from scrapy import FormRequest, cmdline, Request
from scrapy.spiders import CrawlSpider


# from ..items import PlaceDataItem


def getYesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    return yesterday


class WeimaqiSpide(CrawlSpider):
    name = 'weimaqi.net'
    allowed_domains = ['weimaqi.net']
    start_urls = ['https://weimaqi.net/admin_mch_new/login.aspx']
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
    place_items_jscall = []
    place_items = []

    def read_hiddens(self, response):
        event_agent = ''
        event_argument = ''
        view_state = ''
        view_state_navigator = ''
        event_validation = ''
        # 读取各种请求用到的参数
        param_list = response.xpath('//*[@id="__EVENTTARGET"]/@value')
        if len(param_list) > 0:
            event_agent = str(param_list[0].extract())
        param_list = response.xpath('//*[@id="__EVENTARGUMENT"]/@value')
        if len(param_list):
            event_argument = str(param_list[0].extract())
        param_list = response.xpath('//*[@id="__VIEWSTATE"]/@value')
        if len(param_list):
            view_state = str(param_list[0].extract())
        param_list = response.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')
        if len(param_list):
            view_state_navigator = str(param_list[0].extract())
        param_list = response.xpath('//*[@id="__EVENTVALIDATION"]/@value')
        if len(param_list):
            event_validation = str(param_list[0].extract())
        return event_agent, event_argument, view_state, view_state_navigator, event_validation

    def start_requests(self):
        return [Request("https://weimaqi.net/admin_mch_new/login.aspx",
                        callback=self.start_login)]

    def start_login(self, response):
        return [FormRequest.from_response(response,
                                          url='https://weimaqi.net/admin_mch_new/login.aspx',
                                          method='POST',
                                          formdata={},
                                          callback=self.check_person,
                                          dont_filter=True)]

    def check_person(self, response):
        info = json.loads(response.body)
        return [Request('https://weimaqi.net/admin_mch_new/' + str(info[0]['url']),
                        callback=self.handle_check_person)]

    def handle_check_person(self, response):
        (event_agent, event_argument, view_state, view_state_navigator, event_validation) = self.read_hiddens(response)
        # 读取昨日数据
        return [FormRequest.from_response(response,
                                          url="https://weimaqi.net/admin_mch_new/baobiao/turnoverStat.aspx",
                                          method='POST',
                                          formdata={
                                              '__EVENTTARGET': event_agent,
                                              '__EVENTARGUMENT': event_argument,
                                              '__VIEWSTATE': view_state,
                                              '__VIEWSTATEGENERATOR': view_state_navigator,
                                              '__EVENTVALIDATION': event_validation,
                                              'ctl00$ContentPlaceHolder1$txtDateStart': str(getYesterday()),
                                              'ctl00$ContentPlaceHolder1$txtDateEnd': str(getYesterday()),
                                              'ctl00$ContentPlaceHolder1$btnYesterday': '昨日',
                                              'GridView1_length': '100'
                                          },
                                          callback=self.start_read_data,
                                          dont_filter=True)]

    def start_read_data(self, response):
        (event_agent, event_argument, view_state, view_state_navigator, event_validation) = self.read_hiddens(response)
        for sel in response.xpath('//*[@id="GridView1"]/tbody/tr'):
            if len(sel.xpath('td/a[@id="lkbtn_detail"]/@href')) > 0:
                jscall = sel.xpath('td/a[@id="lkbtn_detail"]/@href')[0].extract()
                jscall = str(re.search("\('.+',", jscall).group()[2:-2])
                self.place_items_jscall.append(jscall)
                yield scrapy.FormRequest("https://weimaqi.net/admin_mch_new/baobiao/turnoverStat.aspx",
                                         method='POST',
                                         formdata={
                                             '__EVENTTARGET': jscall,
                                             '__EVENTARGUMENT': event_argument,
                                             '__VIEWSTATE': view_state,
                                             '__VIEWSTATEGENERATOR': view_state_navigator,
                                             '__EVENTVALIDATION': event_validation,
                                             'ctl00$ContentPlaceHolder1$txtDateStart': str(
                                                 getYesterday()),
                                             'ctl00$ContentPlaceHolder1$txtDateEnd': str(getYesterday()),
                                             'GridView1_length': '100'
                                         },
                                         callback=self.read_place_data,
                                         dont_filter=True)

    def read_place_data(self, response):
        pass


cmdline.execute('scrapy runspider WeimaqiSpider.py'.split())
