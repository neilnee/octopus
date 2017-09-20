# coding=utf-8
import scrapy
from ..items import HuxiuItem


class HuxiuSpider(scrapy.Spider):
    name = 'huxiu'
    start_urls = ["https://m.huxiu.com/index.php"]
    allowed_domains = ["huxiu.com"]

    def parse(self, response):
        for sel in response.xpath('//*[@id="list-content"]/div[3]/div[6]/ul/li'):
            item = HuxiuItem()
            # 根据列表项数据类型不同, 区分爬取数据
            # 对于xpath出来的SelectorList, 是list的子类, 所以使用len方法判断大小
            if len(sel.xpath('div[@class="article-hp-info"]')) > 0:
                item['title'] = sel.xpath('div/div/a/h2/span/text()')[0].extract()
                item['link'] = sel.xpath('div/a/@href')[0].extract()
            elif len(sel.xpath('div[@class="article-hp-info article-hp-big-info"]')) > 0:
                item['title'] = sel.xpath('div/a[2]/h2/text()')[0].extract()
                item['link'] = sel.xpath('div/a[2]/@href')[0].extract()
            # 使用response.urlopen方法拼接得到完整链接
            item['link'] = response.urljoin(item['link'])
            # print (item['title'] + '|' + item['link'])
            # 爬取链接内的内容
            yield scrapy.Request(item['link'], callback=self.parse_detail)

    def parse_detail(self, response):
        item = HuxiuItem()
        item['title'] = response.xpath('//*[@id="article"]/div[1]/text()')[0].extract()
        item['link'] = response.url
        # print item['title']
        yield item
