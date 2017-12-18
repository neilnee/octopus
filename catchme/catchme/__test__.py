# coding=utf-8

import json
import urllib2

with open("ch_img.json") as img_file:
    load_ch = json.load(img_file)
    count = 0
    url_all = []
    for i in range(1, 139):
        # url_list = load_ch['machine/qr_code/CATCH_' + str(100000 + i) + '.png']
        url_list = load_ch[str(i)]
        for url in url_list:
            req = urllib2.Request(url)
            # noinspection PyBroadException
            try:
                fd = urllib2.urlopen(req, timeout=0.1)
                print('request finish ' + str(100000 + i) + 'url ' + url)
            except Exception:
                print('request exception ' + str(100000 + i) + ' url ' + url)
            count += 1
    print("total count : " + str(count))

