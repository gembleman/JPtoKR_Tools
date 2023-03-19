import re
import os

path_dir = 'live'
try:
    file_list = os.listdir(path_dir)
except:
    print('error! live 폴더 없나요?')
    os.system('pause')

try:#뉴라이브 폴더 생성 줄
    if not os.path.exists('Newlive'):
        os.makedirs('Newlive')
except:
    print('Newlive 폴더 생성 완료~')
    pass

for l in file_list:
    u = open(path_dir+'\\'+ l, "r",encoding="utf-16")
    yy = re.search('[0-9].+?\.ext',l)
    yy = yy.group()
    try:
        j = open('추출'+yy+'_번역.txt', 'r', encoding="utf-8")
    except:
        print('번역된 파일이 없어요!')
        os.system('pause')
        
    r = open('Newlive\\'+l, 'w', encoding="utf-16")
    
    lines = u.readlines()
    lines2 = j.readlines()
    u.close()
    j.close()
    y = 0
    for line in lines:
        if "[EV_OP:01]" in line:
            t = lines2[y]
            t = t.replace('\n','')
            k = re.sub('(?<=\[◆\]).+?(?=\[◆\])',t,line)#대사 검색
            y += 1
            r.write(k)
        else:
            r.write(line)
    r.close()

print('삽입이 끝났어요 예이~ ^^//')
os.system('pause')
