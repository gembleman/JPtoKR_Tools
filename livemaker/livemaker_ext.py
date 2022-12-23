import pandas as pd
import os
import re
from ast import literal_eval

def main():

    #원문 복원을 위한 딕셔너리 생성.
    kec = open('Hanja(restoration).txt', 'r', encoding='utf-16')
    kec = kec.read()
    kec = kec.replace('\n',',')
    kec = re.sub('(.)(?: <-> )(.)',r'"\2":"\1"', kec)
    kec = "{"+kec+"}"
    k_dic = literal_eval(kec)

    #복원을 위한 함수 정의
    def jap_restore(kk):
        st = ""
        for koll in list(kk):
            if koll in k_dic:
                st = st + k_dic[koll]
            else:
                st = st + koll
        return st


    #대사추출, lsb.txt와 .tsv에서 대사추출
    path_dir = 'Output'
    save_dir = '추출한_대사파일'
    file_list = []

    for path, dirs, files in os.walk(path_dir):
        if not os.path.exists(save_dir+'//'+path):
                os.makedirs(save_dir+'//'+path)
        for file in files:
            coll = os.path.join(path,file)
            file_list.append(coll)

    print('파일 목록 전부 불러옴')
    for list1 in file_list:
        signal = re.search('(.ext.txt|.tsv)$', list1)
        if signal != None:
            if signal.group() == '.tsv':#tsv 파일 추출 줄
                print(list1)
                df = pd.read_csv(list1, sep = '\t', encoding = 'cp949', encoding_errors="surrogateescape")
                for ghu in df.columns:
                    j = re.search('(chr|cha)',ghu)
                    if j != None:
                        file_name = save_dir+'//'+list1+'_'+ghu+'.txt'#찾은 칼럼이 두개 이상일 경우, 따로따로 텍스트파일을 만듬
                        oi = open(file_name,'w', encoding='utf-8', errors='surrogateescape')
                        for ju in df[ghu]:
                            if True == pd.isna(ju):
                                continue
                            else:
                                koll = jap_restore(ju)
                                oi.write(koll+'\n')
                        oi.close()
                        if os.stat(file_name).st_size == 0:#빈 텍스트 파일 삭제.
                            os.remove(file_name)

            if signal.group() == '.ext.txt':#txt 파일 추출 줄
                print(list1)
                jhu = open(list1, 'r', encoding='utf-16', errors='surrogateescape')
                jhu = jhu.readlines()
                oi = open(save_dir+'//'+list1,'w', encoding='utf-8', errors='surrogateescape')
                for jhu1 in jhu:
                    if "[EV_OP:01]" in jhu1:
                        k = re.search('(?<=\[◆\]).+?(?=\[◆\])',jhu1)#대사 검색
                        kk = k.group()
                        kk = kk.replace('(＃)','')#루비 호출문 제거
                        kk = re.sub('\[_IDX_:.+?\]','',kk)#루비 호출문 제거
                        hol = jap_restore(kk)#원문 복원 함수 호출
                        oi.write(hol+'\n')
                oi.close()
                if os.stat(save_dir+'//'+list1).st_size == 0:#빈 텍스트 파일 삭제.
                    os.remove(save_dir+'//'+list1)

    #빈 폴더 삭제.
    paths3 = []
    for path, dirs, files in os.walk(save_dir):
        paths3.append(path)
    for p in reversed(paths3):
        try:
            os.rmdir(p)
        except:
            pass
    print('텍스트 추출 완료~')

if __name__ == '__main__':
    main()
