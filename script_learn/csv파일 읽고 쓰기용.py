import os
import csv
path_dir = 'data'
file_list = os.listdir(path_dir)
with open('word.csv', 'w', newline = '', encoding = 'utf-8') as w:
    wr = csv.writer(w)
    for fl in file_list:
        with open(path_dir+'/'+fl,'r',encoding='utf-8') as f:
            rdr = csv.reader(f)
            for line in rdr:
                wr.writerow([line[0],line[1]])