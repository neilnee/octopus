# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PlaceDataItem(scrapy.Item):
    name = scrapy.Field()  # 场地名称
    income = scrapy.Field()  # 营收
    income_average = scrapy.Field()  # 台均营收
    profit = scrapy.Field()  # 去娃娃盈利
    profit_average = scrapy.Field()  # 台均去娃娃盈利
    probability = scrapy.Field()  # 抓取概率
    num_of_game = scrapy.Field()  # 游戏次数
    gift = scrapy.Field()  # 掉落数量
    coin_buy = scrapy.Field()  # 销售币数
    coin_free = scrapy.Field()  # 派发币数
    device_have_income = scrapy.Field()  # 有营收的机器数量
    device_no_income = scrapy.Field()  # 0营收的机器数量
