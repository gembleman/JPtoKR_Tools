import re
import os
import pandas as pd

path_dir = 'tsv_shift_jis'
save_dir = 'chr&cha열_추출'
file_list = []

for path, dirs, files in os.walk(path_dir):
    for file in files:
        file_list.append(os.path.join(path,file))

if not os.path.exists(save_dir):
    os.makedirs(save_dir)
    print('chr&cha열_추출 폴더 생성 완료~')

for l in file_list:
    df = pd.read_csv(l, sep = '\t', encoding='shift-jis',na_values =['N\A'],encoding_errors="replace")
    xx = pd.DataFrame()
    sin = 0
    print(l)
    for ghu in df.columns:
        j = re.search('(chr|cha)',ghu)
        if j != None:
            print(ghu)
            sin = 1
            ju = df[ghu]
            xx = pd.concat((xx, ju),axis=1)
    if sin == 1:
        l2 = l.split('\\')
        xx.to_csv(save_dir+'//'+l2[-1]+"_추출.txt", sep='$', index=False ,header = None, encoding='utf-8')
print('chr&cha열_추출 완료~ ^^')
os.system('pause')
