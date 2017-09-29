from scrapy import Request
from scrapy.spiders import CrawlSpider


class SettingSpider(CrawlSpider):
    name = 'setting'
    allowed_domains = ['weimaqi.net']
    start_urls = ['https://weimaqi.net/admin_mchm_new/login.html']
    uid = ''
    pwd = ''

    def __init__(self, *args, **kwargs):
        super(SettingSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        return [Request("https://weimaqi.net/admin_mchm_new/login.html",
                        callback=self.start_login)]

    def start_login(self, response):
        pass
