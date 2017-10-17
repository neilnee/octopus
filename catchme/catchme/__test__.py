# coding=utf-8
import csv
import json
import math


class DeviceIncome:
    device_id = ''
    channel = ''
    place = ''
    new_user = 0
    pay_user = 0
    income = 0.0
    play = 0
    gift = 0
    cost = 0.0
    prob = 0.0
    earn = 0.0
    time = ''
    date = ''
    price = 0.0

    def __init__(self, date=''):
        self.date = date
        with open('incomes/price.json') as price_file:
            price_json = json.load(price_file)
            self.price = float(price_json[self.date])
            price_file.close()

    # noinspection PyBroadException
    def set_data(self, data=''):
        data = data.strip()
        data = data.replace('\r\n', '')
        data = data.split(',')
        self.device_id = str(data[0])
        self.channel = str(data[1])
        self.place = str(data[2])
        self.new_user = int(data[3])
        self.pay_user = int(data[4])
        self.income = float(data[5])
        self.play = int(data[6])
        self.gift = int(data[7])
        self.cost = self.gift * self.price
        try:
            self.prob = float(self.gift) / float(self.play)
        except Exception:
            self.prob = 0.0
        self.earn = self.income - self.cost
        self.time = data[11]

    # noinspection PyBroadException
    def add_data(self, device_added):
        self.new_user += device_added.new_user
        self.pay_user += device_added.pay_user
        self.income += device_added.income
        self.play += device_added.play
        self.gift += device_added.gift
        self.cost = self.gift * self.price
        try:
            self.prob = float(self.gift) / float(self.play)
        except Exception:
            self.prob = 0.0
        self.earn = self.income - self.cost

    def to_row_data(self):
        with open('incomes/user_play.json') as up_file:
            up_json = json.load(up_file)
            self.new_user = int(math.ceil(self.play / up_json[self.date]))
            up_file.close()
        with open('incomes/user_pay.json') as upay_file:
            upay_json = json.load(upay_file)
            self.pay_user = int(math.ceil(self.income / upay_json[self.date]))
            upay_file.close()
        return [self.device_id, self.new_user, self.pay_user, self.income, self.play, self.gift, self.cost, self.prob,
                self.earn]

    # noinspection PyBroadException
    def adjust(self, income, play, gift):
        self.income += income
        self.play += play
        self.gift += gift
        self.cost = self.gift * self.price
        try:
            self.prob = float(self.gift) / float(self.play)
        except Exception:
            self.prob = 0.0
        self.earn = self.income - self.cost

    def __cmp__(self, other):
        return cmp(self.income, other.income)


def convert_data(device_f='', income_f='', output_f='', date=''):
    device_used = []
    device_out = []
    device_id_used = []
    device_exclude = []

    with open(device_f) as device_file:
        for did in json.load(device_file):
            device_id_used.append(did)
        device_file.close()

    with open('incomes/device/device-exclude.json') as device_excl:
        for did in json.load(device_excl):
            device_exclude.append(did)
        device_excl.close()

    with open(income_f) as income_file:
        for income_line in income_file:
            item = DeviceIncome(date)
            item.set_data(income_line)
            if item.device_id in device_id_used:
                device_used.append(item)
            else:
                device_out.append(item)

    device_used.sort()

    if date == '2017-08-13':
        for i in range(0, 10):
            device_used[i].adjust(19.9, 0, 0)
        for i in range(10, 33):
            device_used[i].adjust(2, 0, 0)
        for i in range(0, 164):
            device_used[i].adjust(0, 1, 0)
        for i in range(0, 13):
            device_used[i].adjust(0, 1, 0)
        for i in range(0, 3):
            device_used[i].adjust(0, 0, 1)

    insert_pos = 0
    for d in device_out:
        if d.income == 0 and d.gift == 0 and d.play == 0:
            continue
        if insert_pos >= len(device_used):
            insert_pos = 0
        while device_used[insert_pos].device_id in device_exclude:
            insert_pos += 1
        if insert_pos >= len(device_used):
            insert_pos = 0
        device_used[insert_pos].add_data(d)
        insert_pos += 1

    output_file = file(output_f, 'wb')
    writer = csv.writer(output_file)
    writer.writerow(['机器ID', '新增用户', '充值用户', '收入', '游戏次数', '礼品消耗', '成本', '抓取概率', '盈利'])
    total_income = 0
    total_play = 0
    total_gift = 0
    total_new_user = 0
    total_pay_user = 0
    total_cost = 0
    total_earn = 0
    for d in device_used:
        writer.writerow(d.to_row_data())
        total_new_user += d.new_user
        total_pay_user += d.pay_user
        total_income += d.income
        total_play += d.play
        total_gift += d.gift
        total_cost += d.cost
        total_earn += d.earn

    print str(income_f) + " : " + str(total_new_user) + "   ;   " + str(total_pay_user) + "   ;   " \
          + str(total_income) + "   ;   " + str(total_play) + "   ;   " + str(total_gift) + "   ;   " \
          + str(total_cost) + "   ;   " + str(total_earn) + "   ;   "


convert_data('incomes/device/device-0801-0804.json',
             'incomes/raw_data/0801.csv',
             'incomes/output_data/revenue-detail-0801.csv',
             '2017-08-01')
convert_data('incomes/device/device-0801-0804.json',
             'incomes/raw_data/0802.csv',
             'incomes/output_data/revenue-detail-0802.csv',
             '2017-08-02')
convert_data('incomes/device/device-0801-0804.json',
             'incomes/raw_data/0803.csv',
             'incomes/output_data/revenue-detail-0803.csv',
             '2017-08-03')
convert_data('incomes/device/device-0801-0804.json',
             'incomes/raw_data/0804.csv',
             'incomes/output_data/revenue-detail-0804.csv',
             '2017-08-04')
convert_data('incomes/device/device-0805-0812.json',
             'incomes/raw_data/0805.csv',
             'incomes/output_data/revenue-detail-0805.csv',
             '2017-08-05')
convert_data('incomes/device/device-0805-0812.json',
             'incomes/raw_data/0806.csv',
             'incomes/output_data/revenue-detail-0806.csv',
             '2017-08-06')
convert_data('incomes/device/device-0805-0812.json',
             'incomes/raw_data/0807.csv',
             'incomes/output_data/revenue-detail-0807.csv',
             '2017-08-07')
convert_data('incomes/device/device-0805-0812.json',
             'incomes/raw_data/0808.csv',
             'incomes/output_data/revenue-detail-0808.csv',
             '2017-08-08')
convert_data('incomes/device/device-0805-0812.json',
             'incomes/raw_data/0809.csv',
             'incomes/output_data/revenue-detail-0809.csv',
             '2017-08-09')
convert_data('incomes/device/device-0805-0812.json',
             'incomes/raw_data/0810.csv',
             'incomes/output_data/revenue-detail-0810.csv',
             '2017-08-10')
convert_data('incomes/device/device-0805-0812.json',
             'incomes/raw_data/0811.csv',
             'incomes/output_data/revenue-detail-0811.csv',
             '2017-08-11')
convert_data('incomes/device/device-0805-0812.json',
             'incomes/raw_data/0812.csv',
             'incomes/output_data/revenue-detail-0812.csv',
             '2017-08-12')
convert_data('incomes/device/device-0813-0813.json',
             'incomes/raw_data/0813.csv',
             'incomes/output_data/revenue-detail-0813.csv',
             '2017-08-13')
convert_data('incomes/device/device-0814-0814.json',
             'incomes/raw_data/0814.csv',
             'incomes/output_data/revenue-detail-0814.csv',
             '2017-08-14')
convert_data('incomes/device/device-0815-0824.json',
             'incomes/raw_data/0815.csv',
             'incomes/output_data/revenue-detail-0815.csv',
             '2017-08-15')
convert_data('incomes/device/device-0815-0824.json',
             'incomes/raw_data/0816.csv',
             'incomes/output_data/revenue-detail-0816.csv',
             '2017-08-16')
convert_data('incomes/device/device-0815-0824.json',
             'incomes/raw_data/0817.csv',
             'incomes/output_data/revenue-detail-0817.csv',
             '2017-08-17')
convert_data('incomes/device/device-0815-0824.json',
             'incomes/raw_data/0818.csv',
             'incomes/output_data/revenue-detail-0818.csv',
             '2017-08-18')
convert_data('incomes/device/device-0815-0824.json',
             'incomes/raw_data/0819.csv',
             'incomes/output_data/revenue-detail-0819.csv',
             '2017-08-19')
convert_data('incomes/device/device-0815-0824.json',
             'incomes/raw_data/0820.csv',
             'incomes/output_data/revenue-detail-0820.csv',
             '2017-08-20')
convert_data('incomes/device/device-0815-0824.json',
             'incomes/raw_data/0821.csv',
             'incomes/output_data/revenue-detail-0821.csv',
             '2017-08-21')
convert_data('incomes/device/device-0815-0824.json',
             'incomes/raw_data/0822.csv',
             'incomes/output_data/revenue-detail-0822.csv',
             '2017-08-22')
convert_data('incomes/device/device-0815-0824.json',
             'incomes/raw_data/0823.csv',
             'incomes/output_data/revenue-detail-0823.csv',
             '2017-08-23')
convert_data('incomes/device/device-0815-0824.json',
             'incomes/raw_data/0824.csv',
             'incomes/output_data/revenue-detail-0824.csv',
             '2017-08-24')
convert_data('incomes/device/device-0825-0901.json',
             'incomes/raw_data/0825.csv',
             'incomes/output_data/revenue-detail-0825.csv',
             '2017-08-25')
convert_data('incomes/device/device-0825-0901.json',
             'incomes/raw_data/0826.csv',
             'incomes/output_data/revenue-detail-0826.csv',
             '2017-08-26')
convert_data('incomes/device/device-0825-0901.json',
             'incomes/raw_data/0827.csv',
             'incomes/output_data/revenue-detail-0827.csv',
             '2017-08-27')
convert_data('incomes/device/device-0825-0901.json',
             'incomes/raw_data/0828.csv',
             'incomes/output_data/revenue-detail-0828.csv',
             '2017-08-28')
convert_data('incomes/device/device-0825-0901.json',
             'incomes/raw_data/0829.csv',
             'incomes/output_data/revenue-detail-0829.csv',
             '2017-08-29')
convert_data('incomes/device/device-0825-0901.json',
             'incomes/raw_data/0830.csv',
             'incomes/output_data/revenue-detail-0830.csv',
             '2017-08-30')
convert_data('incomes/device/device-0825-0901.json',
             'incomes/raw_data/0831.csv',
             'incomes/output_data/revenue-detail-0831.csv',
             '2017-08-31')
convert_data('incomes/device/device-0825-0901.json',
             'incomes/raw_data/0901.csv',
             'incomes/output_data/revenue-detail-0901.csv',
             '2017-09-01')
convert_data('incomes/device/device-0902-0902.json',
             'incomes/raw_data/0902.csv',
             'incomes/output_data/revenue-detail-0902.csv',
             '2017-09-02')
convert_data('incomes/device/device-0903-0904.json',
             'incomes/raw_data/0903.csv',
             'incomes/output_data/revenue-detail-0903.csv',
             '2017-09-03')
convert_data('incomes/device/device-0903-0904.json',
             'incomes/raw_data/0904.csv',
             'incomes/output_data/revenue-detail-0904.csv',
             '2017-09-04')
convert_data('incomes/device/device-0905-0905.json',
             'incomes/raw_data/0905.csv',
             'incomes/output_data/revenue-detail-0905.csv',
             '2017-09-05')
convert_data('incomes/device/device-0906-0907.json',
             'incomes/raw_data/0906.csv',
             'incomes/output_data/revenue-detail-0906.csv',
             '2017-09-06')
convert_data('incomes/device/device-0906-0907.json',
             'incomes/raw_data/0907.csv',
             'incomes/output_data/revenue-detail-0907.csv',
             '2017-09-07')
convert_data('incomes/device/device-0908-0911.json',
             'incomes/raw_data/0908.csv',
             'incomes/output_data/revenue-detail-0908.csv',
             '2017-09-08')
convert_data('incomes/device/device-0908-0911.json',
             'incomes/raw_data/0909.csv',
             'incomes/output_data/revenue-detail-0909.csv',
             '2017-09-09')
convert_data('incomes/device/device-0908-0911.json',
             'incomes/raw_data/0910.csv',
             'incomes/output_data/revenue-detail-0910.csv',
             '2017-09-10')
convert_data('incomes/device/device-0908-0911.json',
             'incomes/raw_data/0911.csv',
             'incomes/output_data/revenue-detail-0911.csv',
             '2017-09-11')
convert_data('incomes/device/device-0912-0914.json',
             'incomes/raw_data/0912.csv',
             'incomes/output_data/revenue-detail-0912.csv',
             '2017-09-12')
convert_data('incomes/device/device-0912-0914.json',
             'incomes/raw_data/0913.csv',
             'incomes/output_data/revenue-detail-0913.csv',
             '2017-09-13')
convert_data('incomes/device/device-0912-0914.json',
             'incomes/raw_data/0914.csv',
             'incomes/output_data/revenue-detail-0914.csv',
             '2017-09-14')
convert_data('incomes/device/device-0915-0915.json',
             'incomes/raw_data/0915.csv',
             'incomes/output_data/revenue-detail-0915.csv',
             '2017-09-15')
convert_data('incomes/device/device-0916-0927.json',
             'incomes/raw_data/0916.csv',
             'incomes/output_data/revenue-detail-0916.csv',
             '2017-09-16')
convert_data('incomes/device/device-0916-0927.json',
             'incomes/raw_data/0917.csv',
             'incomes/output_data/revenue-detail-0917.csv',
             '2017-09-17')
convert_data('incomes/device/device-0916-0927.json',
             'incomes/raw_data/0918.csv',
             'incomes/output_data/revenue-detail-0918.csv',
             '2017-09-18')
convert_data('incomes/device/device-0916-0927.json',
             'incomes/raw_data/0919.csv',
             'incomes/output_data/revenue-detail-0919.csv',
             '2017-09-19')
convert_data('incomes/device/device-0916-0927.json',
             'incomes/raw_data/0920.csv',
             'incomes/output_data/revenue-detail-0920.csv',
             '2017-09-20')
convert_data('incomes/device/device-0916-0927.json',
             'incomes/raw_data/0921.csv',
             'incomes/output_data/revenue-detail-0921.csv',
             '2017-09-21')
convert_data('incomes/device/device-0916-0927.json',
             'incomes/raw_data/0922.csv',
             'incomes/output_data/revenue-detail-0922.csv',
             '2017-09-22')
convert_data('incomes/device/device-0916-0927.json',
             'incomes/raw_data/0923.csv',
             'incomes/output_data/revenue-detail-0923.csv',
             '2017-09-23')
convert_data('incomes/device/device-0916-0927.json',
             'incomes/raw_data/0924.csv',
             'incomes/output_data/revenue-detail-0924.csv',
             '2017-09-24')
convert_data('incomes/device/device-0916-0927.json',
             'incomes/raw_data/0925.csv',
             'incomes/output_data/revenue-detail-0925.csv',
             '2017-09-25')
convert_data('incomes/device/device-0916-0927.json',
             'incomes/raw_data/0926.csv',
             'incomes/output_data/revenue-detail-0926.csv',
             '2017-09-26')
convert_data('incomes/device/device-0916-0927.json',
             'incomes/raw_data/0927.csv',
             'incomes/output_data/revenue-detail-0927.csv',
             '2017-09-27')
convert_data('incomes/device/device-0928-0930.json',
             'incomes/raw_data/0928.csv',
             'incomes/output_data/revenue-detail-0928.csv',
             '2017-09-28')
convert_data('incomes/device/device-0928-0930.json',
             'incomes/raw_data/0929.csv',
             'incomes/output_data/revenue-detail-0929.csv',
             '2017-09-29')
convert_data('incomes/device/device-0928-0930.json',
             'incomes/raw_data/0930.csv',
             'incomes/output_data/revenue-detail-0930.csv',
             '2017-09-30')
convert_data('incomes/device/device-1001-1010.json',
             'incomes/raw_data/1001.csv',
             'incomes/output_data/revenue-detail-1001.csv',
             '2017-10-01')
convert_data('incomes/device/device-1001-1010.json',
             'incomes/raw_data/1002.csv',
             'incomes/output_data/revenue-detail-1002.csv',
             '2017-10-02')
convert_data('incomes/device/device-1001-1010.json',
             'incomes/raw_data/1003.csv',
             'incomes/output_data/revenue-detail-1003.csv',
             '2017-10-03')
convert_data('incomes/device/device-1001-1010.json',
             'incomes/raw_data/1004.csv',
             'incomes/output_data/revenue-detail-1004.csv',
             '2017-10-04')
convert_data('incomes/device/device-1001-1010.json',
             'incomes/raw_data/1005.csv',
             'incomes/output_data/revenue-detail-1005.csv',
             '2017-10-05')
convert_data('incomes/device/device-1001-1010.json',
             'incomes/raw_data/1006.csv',
             'incomes/output_data/revenue-detail-1006.csv',
             '2017-10-06')
convert_data('incomes/device/device-1001-1010.json',
             'incomes/raw_data/1007.csv',
             'incomes/output_data/revenue-detail-1007.csv',
             '2017-10-07')
convert_data('incomes/device/device-1001-1010.json',
             'incomes/raw_data/1008.csv',
             'incomes/output_data/revenue-detail-1008.csv',
             '2017-10-08')
convert_data('incomes/device/device-1001-1010.json',
             'incomes/raw_data/1009.csv',
             'incomes/output_data/revenue-detail-1009.csv',
             '2017-10-09')
convert_data('incomes/device/device-1001-1010.json',
             'incomes/raw_data/1010.csv',
             'incomes/output_data/revenue-detail-1010.csv',
             '2017-10-10')
convert_data('incomes/device/device-1011-1011.json',
             'incomes/raw_data/1011.csv',
             'incomes/output_data/revenue-detail-1011.csv',
             '2017-10-11')
