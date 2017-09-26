from scrapy.spiders import CrawlSpider


class SettingSpider(CrawlSpider):

    def __init__(self, *args, **kwargs):
        super(SettingSpider, self).__init__(*args, **kwargs)
