import re
import os
import pandas as pd
from ast import literal_eval

#Hanja.txt를 기반으로 원문으로 역변환 시킨다. 원문 파일이 필요없어지니 작업을 한 단계 줄일 수 있음.
try:
    kec = open('Hanja.txt', 'r', encoding='utf-16')
except:
    print('Hanja.txt 파일이 없나요???')
    os.system('pause')

kec = kec.read()
kec = kec.replace('\n',',')
kec = re.sub('(.)(?: <-> )(.)',r'"\2":"\1"', kec)
kec = "{"+kec+"}"
kec = literal_eval(kec)
#원문 복원용 매칭표 만듬-----|-|-

path_dir = 'tsv_cp949'
save_dir = 'tsv_chr_cha열_추출'
file_list = []
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
    print('tsv_chr_cha열_추출 폴더 생성 완료~')

for path, dirs, files in os.walk(path_dir):
    path2 = path.replace('tsv_cp949','')
    if not os.path.exists(save_dir+'//'+path2):
        os.makedirs(save_dir+'//'+path2)
    for file in files:
        file_list.append(os.path.join(path, file))

for l in file_list:
    df = pd.read_csv(l, sep = '\t', encoding='cp949',na_values =['N\A'],encoding_errors="surrogateescape")
    print(l)
    for ghu in df.columns:
        j = re.search('(chr|cha)',ghu)
        if j != None:
            l2 = l.replace('tsv_cp949','')
            txt_dir = save_dir+'//'+l2+'_'+ghu+"_추출.txt"
            oi = open(txt_dir, 'w', encoding='utf-8', errors="surrogateescape")
            print(ghu)
            #cp949에 든 내용을 shift-jis로 복원함.
            #문장의 음절들을 하나하나 대조하는 방식밖에 없고 그래서 느려질 수 있음.
            for ju in df[ghu]:
                if True == pd.isna(ju):
                    continue
                st = ""
                for lit in list(ju):#문장을 하나의 음절로 쪼갬
                    if lit in kec:#변환할 음절인지 검사
                        st = st+kec[lit]#변환한 문자 추가
                    else:
                        st = st+lit
                oi.write(st+'\n')
                #나중에 번역 기능도 넣으면 좋을 듯.
            oi.close()
            if os.stat(txt_dir).st_size == 0:#빈 텍스트파일 제거
                os.remove(txt_dir)

print('tsv_chr_cha열_추출 완료~ ^^')
os.system('pause')
