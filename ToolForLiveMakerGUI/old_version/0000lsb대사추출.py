import re
import os

path_dir = 'live'
try:
    file_list = os.listdir(path_dir)
except:
    print('error! live 폴더 없나요?')
    os.system('pause')

for l in file_list:
    u = open(path_dir+'\\'+ l, "r",encoding="utf-16")
    j = open('추출'+l, 'w', encoding="utf-8")
    lines = u.readlines()
    for line in lines:
        if "[EV_OP:01]" in line:
            k = re.search('(?<=\[◆\]).+?(?=\[◆\])',line)#대사 검색
            kk = k.group()
            kk = kk.replace('(＃)','')#루비 호출문 제거
            kk = re.sub('\[_IDX_:.+?\]','',kk)#루비 호출문 제거
            j.write(kk+'\n')
            
    j.close()
    u.close()

print('추출이 끝났어요 예이~ ^^//')
os.system('pause')
