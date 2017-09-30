import hashlib
import random

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

        print ('uid=' + uid + '; pwd=' + pwd)

    def start_requests(self):
        return [Request("https://weimaqi.net/admin_mchm_new/login.html",
                        callback=self.start_login)]

    def start_login(self, response):
        return [FormRequest.from_response(response,
                                          url='https://weimaqi.net/admin_mchm_new/control/Handler.ashx?action=login',
                                          method='POST',
                                          formdata={
                                              'mch_acc': self.uid,
                                              'mch_pwd': hashlib.md5(hashlib.md5(self.pwd).hexdigest().upper()).hexdigest(),
                                              'auto': 'false'},
                                          callback=self.check_info,
                                          dont_filter=True)]

    def check_info(self, response):
        return [Request('https://weimaqi.net/admin_mchm_new/CheckInfo_m.aspx?r=' + str(random.random()),
                        callback=self.handle_check_info)]

    def handle_check_info(self, response):
        pass
