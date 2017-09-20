import re

from scrapy import FormRequest, cmdline, Request
from scrapy.spiders import CrawlSpider


class WeimaqiSpide(CrawlSpider):
    name = 'weimaqi.net'
    allowed_domains = ['weimaqi.net']
    # start_urls = ['https://weimaqi.net/admin_mch_new/login.aspx']
    headers = {
        "Connection": "keep-alive",
        "Content-Length": "37",
        "Accept": "*/*",
        "Origin": "https://weimaqi.net",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Mobile Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Referer": "https://weimaqi.net/admin_mch_new/login.aspx",
        "Accept - Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
    }
    cookies = {
        'ASP.NET_SessionId': 'jw1fvvcuc40pcmqwnsbh0hs2',
        'SERVERID': '69fdaa4572acfae6295ffc289cece7b6|1505819581|1505409732'
    }

    def start_requests(self):
        print 'func start_requests start'
        return [Request("https://weimaqi.net/admin_mch_new/login.aspx", callback=self.start_login)]

    def start_login(self, response):
        headerstr = str(response.headers)
        print "func start_login: " + headerstr
        print(re.search('ASP.NET_SessionId=.+;', headerstr).span())
        # return [FormRequest.from_response(response,
        #                                   url='https://weimaqi.net/admin_mch_new/login.aspx',
        #                                   headers=self.headers,
        #                                   formdata={'uid': 'catch4yaolai', 'pwd': 'catchme@5107yl'},
        #                                   cookies=self.cookies,
        #                                   callback=self.check_person,
        #                                   # meta={'cookiejar': response.meta['cookiejar']},
        #                                   dont_filter=True)]

    def check_person(self, response):
        print "func check_person start: " + str(response.meta['cookiejar'])

cmdline.execute('scrapy runspider WeimaqiSpider.py'.split())
