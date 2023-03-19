import pandas as pd
import os
import re
import sys


def main():

    # 1.추출한_대사파일 폴더에 든 텍스트 파일 읽어들이기
    # 2.Output 폴더에서 매칭되는 파일 찾기.
    # 3. 파일에 번역문 삽입

    path_dir = "추출한_대사파일"
    file_list = []
    for path, dirs, files in os.walk(path_dir):  # chr,cha열 추출 폴더에서 "_번역" 파일만 읽어들이기.
        for file in files:
            if "_번역" in file:
                file_list.append(os.path.join(path, file))
    tsv_list = (
        []
    )  # tsv 파일에 chr, cha 열이 하나가 아닌 경우, 그런 열이 들어간 번역 파일은 다시 불러오지 않도록 한다. 그것을 위한 리스트
    for list in file_list:
        qq = re.search("(\.ext_번역\.txt|\.tsv.+?_번역\.txt)$", list)
        if qq != None:
            if ".tsv_" in qq.group():  # tsv 번역 파일 관련 줄
                if list in tsv_list:
                    print("중복")
                    continue
                print("--------tsv파일 감지-------")
                # 원본 파일 읽기.
                red = re.sub("(추출한_대사파일\\\\|(?<=.tsv)_.+?_번역.txt)", "", list)
                df = pd.read_csv(
                    red, sep="\t", encoding="CP949", encoding_errors="surrogateescape"
                )
                print("tsv파일: " + red)
                # chr, cha로 된 열 감지.
                col_list = []  # cha, chr 칼럼명 리스트
                for ghu in df.columns:  # 칼럼명 수집.
                    ff = re.search("(chr|cha)", ghu)
                    if ff != None:
                        col_list.append(ghu)

                print("-----칼럼명 검사중-----")
                for koul in col_list:
                    if (
                        koul not in list
                    ):  # tsv파일에 열이름 중 chr, cha가 들어간 열이 하나가 아닌 경우, 해당 열의 번역파일도 불러오는데, 그것을 나중에 다시 불러오는 걸 막기 위해, 리스트로 저장.
                        list = re.sub(
                            "(?<=.tsv)_.+?(_번역.txt)", r"_" + koul + r"\1", list
                        )
                        tsv_list.append(list)  # 다시 불러오는 걸 막기위한 리스트 저장.
                    print("번역한 파일 읽기:" + list)
                    # 번역한 파일 읽기.
                    try:
                        deric = open(list, "r", encoding="utf-8-sig")
                    except OSError as inst:
                        type_, value, traceback_ = sys.exc_info()
                        if "[Errno 2] No such file or directory:" in str(
                            value
                        ):  # 이 에러가 발생되는 건, 추출할 때, 빈 chr,cha열은 그 열의 이름으로 된 텍스트파일을 저장하지 않기 때문.
                            for number, ju in enumerate(df[koul]):
                                if True != pd.isna(ju):  # 빈칸이 아닌 칸이 하나라도 나올 경우
                                    print(
                                        "추출과정에서 뭔가 잘못됐네요. 멈춥니다."
                                    )  # 추출할 때, 모든 줄을 완벽하게 추출했다면 이런 경우는 발생하지 않음.
                                    os.system("pause")
                            print("이 세로열은 비었습니다. 넘어갑니다.")
                            continue

                    deric1 = deric.readlines()
                    deric.close()
                    n = 0
                    # 번역문으로 교체하는 줄.
                    for number, ju in enumerate(df[koul]):
                        if True != pd.isna(ju):  # 빈칸은 넘어가기
                            deco = deric1[n].replace("\n", "")
                            if ju == deco:  # 변화 없으면 넘어가기
                                continue
                            df.loc[number, koul] = deco
                            n += 1
                        else:
                            continue
                print("번역문으로 교체성공")
                # tsv 파일에 대사를 추출해도 거기에 번역해서는 안되는 명령줄이 포함되어 있는 경우가 있음.
                # ehnd 사전 추가도 해야됨. /大文字/,/搖れ/,/出題/
                df.to_csv(
                    red,
                    sep="\t",
                    index=False,
                    encoding="cp949",
                    errors="surrogateescape",
                )

            if qq.group() == ".ext_번역.txt":  # txt 번역 파일 관련 줄
                print("-----txt파일 감지-----")
                print("lsb 번역용 txt파일:" + list)
                # 번역문 파일 읽기
                uyt = open(list, "r", encoding="utf-8-sig")
                uyt1 = uyt.readlines()
                uyt.close()
                # 원문 파일 읽기
                red = re.sub("(추출한_대사파일\\\\|_번역)", "", list)
                r = open(red, "r", encoding="utf-16")
                r1 = r.readlines()
                r.close()
                y = 0
                for i, line in enumerate(r1):
                    if "[EV_OP:01]" in line:
                        t = uyt1[y].replace("\n", "")
                        k = re.sub(
                            "(?<=\[◆\]).+?(?=\[◆\])", t, line
                        )  # 대사 검색 후 번역문으로 교체
                        y += 1
                        if r1[i] == k:  # 바꿀 문장이 같을 경우, 넘어간다. #이전과 다른 값만 바꾼다.
                            continue
                        else:
                            r1[i] = k  # 번역문 삽입
                print("번역문으로 교체성공")
                # 교체한 파일내용을 이제 기존 파일에다 덮어씌운다.
                r = open(red, "w", encoding="utf-16")
                for r2 in r1:
                    r.write(r2)
                r.close()

    print("tsv, txt 파일 교체 완료~ ^^")


if __name__ == "__main__":
    main()
