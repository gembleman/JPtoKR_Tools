import pandas as pd
import re
from pathlib import Path
import pickle


# Hanja(restoration).txt를 필요 없게 만듬. 원래는 일본어 인코딩 파일에서 원문을 추출해 번역하면, 나중에 한국어 인코딩된 파일 안에다 어느 부분에 넣어야 할지 지정하기 힘들어 기존에는 할 수 없었다.
# 기존 방식 - 1. 원문 파일 인코딩 변환 2.한국어 인코딩된 파일에서 스크립트 추출 및 인코딩 과정에서 손상된 스크립트를 Hanja(restoration).txt를 이용해 원문으로 복원. 3. 번역문을 한국어 인코딩된 파일에 삽입.
# 개선된 방식 1.원문 파일에서 스크립트 추출, 어느 부분에서 추출했는지 좌표 저장. 2.원문 번역. 3. 원문 파일 인코딩 변환 4.저장된 좌표를 활용해 한국어 인코딩된 파일에 번역문을 정확한 위치에다 삽입.

# 좌표는 먼저 줄 위치를 저장하고 그 줄에서 몇번째부터 몇번째까지가 대사 부분인지 파악하고 번호를 저장.
def main(folder_path):

    print("추출 프로세스 진입")
    # 대사추출, lsb.txt와 .tsv에서 대사추출
    path_dir = folder_path / "Output"
    # 여기에다 작업 폴더 경로를 추가해줘야 함.#todo 작업폴더를 사용자설정으로 돌려도 이 코드가 실행이 잘 되는지 확인해야 함.
    save_dir = folder_path / "추출한_대사파일"
    save_dir.mkdir(exist_ok=True)  # 폴더 생성
    print(str(path_dir))
    print(str(save_dir))

    for list1 in list(path_dir.glob("**")):
        # output 폴더에 있는 폴더 트리를 추출한_대사파일 폴더에 복제.
        makedir = save_dir / list1.relative_to(path_dir)
        makedir.mkdir(exist_ok=True)

    # print("파일 목록 전부 불러옴")
    esb_dic = {}  # esb 파일 위치값 저장용
    tsv_dic = {}  # tsv 파일 위치값 저장용
    for list1 in list(path_dir.glob("**/*")):
        signal = re.search("(.ext.txt|.tsv)$", list1.name)
        if signal != None:

            if signal.group() == ".tsv":  # tsv 파일 추출 줄
                print(str(list1))
                df = pd.read_csv(
                    list1, sep="\t", encoding="cp932", encoding_errors="surrogateescape"
                )
                columns_list = []
                flag = 0
                for ghu in df.columns:

                    if re.search("(chr|cha)", ghu):
                        # tsv 피클 저장 형식 -> {파일이름 : [열이름들]} 열이름 저장. 셀 위치는 저장하지 않음..
                        lll = str(list1.relative_to(path_dir)) + "_" + ghu + "_추출.txt"
                        file_name = save_dir / lll
                        # 찾은 칼럼이 두개 이상일 경우, 따로따로 텍스트파일을 만듬 - 칼럼명이 파일명인 텍스트 파일을 만듬.
                        with open(
                            file_name,
                            "w",
                            encoding="utf-8",
                            errors="surrogateescape",
                        ) as oi:
                            for ju in df[ghu]:  # 해당 열에 있는 셀 나열.
                                if True == pd.isna(ju):  # 값이 비어있는 셀인지 확인.
                                    continue
                                else:
                                    oi.write(ju + "\n")

                        if file_name.stat().st_size == 0:  # 빈 텍스트 파일 삭제.
                            file_name.unlink()  # pathlib을 써서 파일 삭제.
                        else:
                            columns_list.append(ghu)  # 해당하는 열이름 저장
                            flag = 1
                if flag == 1:
                    tsv_dic[list1] = columns_list

            if signal.group() == ".ext.txt":  # txt 파일 추출 줄
                coo_dic = {}  # 원문 좌표값 저장용
                print(str(list1))
                # https://stackoverflow.com/questions/59993320/python-pathlib-how-do-i-remove-leading-directories-to-get-relative-paths
                lll = str(list1.relative_to(path_dir)) + "_추출.txt"
                save_dir2 = save_dir / lll
                # pathlib으로 상대경로를 얻고 싶을 때.
                with open(
                    list1, "r", encoding="utf-16", errors="surrogateescape"
                ) as jhu:
                    jhu23 = jhu.readlines()
                list45 = []
                for line_num, jhu2 in enumerate(jhu23):
                    # 스크립트 감별
                    if "[EV_OP:01]" in jhu2:
                        k = re.search("(?<=\[◆\]).+?(?=\[◆\])", jhu2)  # 대사 검색
                        coo = k.span()  # 원문 위치 저장용 - 나중에 번역문 삽입할 때 쓰임.
                        # line_num 원문 줄 수 저장용
                        coo_dic[line_num] = coo  # 사전에 추가.
                        # esb 원문 위치 저장 방식 : {파일이름 : {줄위치 : 스크립트 위치,줄위치 : 스크립트 위치,줄위치 : 스크립트 위치,줄위치 : 스크립트 위치 ...}}
                        kk = k.group()
                        kk = kk.replace("(＃)", "")  # 루비 호출문 제거
                        kk = re.sub("\[_IDX_:.+?\]", "", kk)  # 루비 호출문 제거
                        # 원문 복원 함수 호출 - Toolfor라이브메이커 로케일 과정을 이전에 거쳤기 때문에 다시 원문 복원이 필요하게 됨. - 더 최적화 시킬 수 없을까? - 01.15. 로케일 변환 이전에 추출.
                        list45.append(kk + "\n")  # 추출문 저장.

                with open(
                    save_dir2, "w", encoding="utf-8", errors="surrogateescape"
                ) as oi:
                    oi.writelines(list45)

                if save_dir2.stat().st_size == 0:  # 빈 텍스트 파일 삭제.
                    save_dir2.unlink()  # pathlib을 써서 파일 삭제.
                else:
                    esb_dic[list1] = coo_dic

    with open(folder_path / "coordinate.pickle", "wb") as coordinate:
        # 추출한 원문의 위치값 저장용
        pickle.dump([tsv_dic, esb_dic], coordinate)

    # 빈 폴더 삭제.
    for list1 in reversed(list(save_dir.glob("**"))):
        try:
            list1.rmdir()
        except:
            pass

    print("텍스트 추출 완료~")


if __name__ == "__main__":
    print("라이브메이커 추출 모듈입니다.")
