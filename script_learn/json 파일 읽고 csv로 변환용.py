import json
import os
import csv

path_dir = 'data'
file_list = os.listdir(path_dir)
with open('word_join_va2.csv', 'w', newline = '', encoding = 'utf-8') as w:
    wr = csv.writer(w)
    for fl in file_list:
        with open(path_dir+'/'+fl, 'r', encoding = 'utf-8') as f:
            jami = json.load(f)#json 자료 형식에 따라 아랫줄은 달라짐.
            for jl in jami["data"]:
                try:
                    wr.writerow([jl['jp'],jl['ko']])
                except:
                    print(jl)
                    quit()
