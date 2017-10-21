# coding=utf-8
import time

day1 = '2017-10-21'
day2 = '2017-10-22'

td1 = time.strptime(day1, '%Y-%m-%d')
td2 = time.strptime(day2, '%Y-%m-%d')

print td1 <= td2

