# coding=utf-8

from openpyxl import load_workbook

wb = load_workbook('revenue/catchme_ch/revenue_2017-12-09_ch.xlsx')

ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])

for row in ws.rows:
    print(row[3].value)

