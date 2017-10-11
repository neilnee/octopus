# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# 场地营收
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


# 设置
class SettingItem(scrapy.Item):
    d_name = scrapy.Field()  # 设备编号
    device_id = scrapy.Field()  # 设备内部ID
    tag = scrapy.Field()  # 设备标签(渠道)
    des = scrapy.Field()  # 设备备注
    online = scrapy.Field()  # 是否在线,
    setting_param = scrapy.Field()  # 设置参数 num0_1
    coin_per_time = scrapy.Field()  # 几投一玩 num1_1
    game_duration = scrapy.Field()  # 游戏时间 num2_1
    music = scrapy.Field()  # 背景音乐 num3_1
    air_pick = scrapy.Field()  # 空中取物 num4_1
    out_pos = scrapy.Field()  # 礼品出口 num5_1
    shake_clear = scrapy.Field()  # 摇晃清分 num6_1
    music_volume = scrapy.Field()  # 音乐大小 num7_1
    free_for_continue = scrapy.Field()  # 连投送币 num8_1
    strong_force = scrapy.Field()  # 强抓力调整 num9_1
    weak_force = scrapy.Field()  # 弱抓力调整 num10_1
    pick_height = scrapy.Field()  # 抓起高度 num11_1
    strong_to_weak = scrapy.Field()  # 强抓变弱抓方式 num12_1
    line_height = scrapy.Field()  # 下抓线长度 num13_1
    out_mode = scrapy.Field()  # 出礼品调整 num14_1
    probability = scrapy.Field()  # N次出一个 num15_1
    eyes = scrapy.Field()  # 光眼有无 num16_1
    keep = scrapy.Field()  # 保送功能 num17_1
    account_clear = scrapy.Field()  # 账目清空 num18_1
    reset = scrapy.Field()  # 恢复出厂 num19_1
    disable_btn = scrapy.Field()  # 禁止线下设置和免费钮 num20_1
    disable_board = scrapy.Field()  # 禁止主板运行 num21_1
