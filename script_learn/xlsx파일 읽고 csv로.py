from openpyxl import load_workbook
import os
import csv

file_list = os.listdir('스크립트_엑셀')
with open('word2.csv', 'w', newline = '', encoding = 'utf-8') as w:
    wr = csv.writer(w)
    for fl in file_list:
        load_wb = load_workbook("스크립트_엑셀/"+fl)
        load_ws = load_wb['시트1']
        for cell_obj, cell_obj2 in zip(list(load_ws.columns)[0],list(load_ws.columns)[1]):
            wr.writerow([cell_obj.value,cell_obj2.value])