from scrapy.spiders import CrawlSpider


class CatchMeSpider(CrawlSpider):
    name = 'catchme'
    allowed_domains = ['catchme.com.cn']
    start_urls = ['http://console.catchme.com.cn/admin/auth/login']

    uid = ''
    pwd = ''

    def __init__(self, uid='', pwd='', *args, **kwargs):
        super(CatchMeSpider, self).__init__(*args, **kwargs)
        self.uid = uid
        self.pwd = pwd


