import re
import pathlib
import pickle

# 원본 파일에서 추출할 줄의 위치값을 저장한다.
ext_dic = {}

path_dir = pathlib.Path("script")
save_dir = pathlib.Path("ext_script")
save_dir.mkdir(exist_ok=True)  # 저장할 폴더 생성.
for dir in path_dir.glob("**/*.ast"):
    print(dir)
    with open(dir, "r", encoding="utf-8") as fff:
        fff1 = fff.readlines()
    fff1 = iter(fff1)
    save_dir2 = save_dir / pathlib.Path(dir.stem + ".txt")

    with open(save_dir2, "w", encoding="utf-8") as save_txt:
        line_num = 0
        linenum_list = []
        for bb in fff1:
            # 대사문, 설명문 추출
            if "\t\t\tja = {\n" == bb or "\t\t\tja={\n" == bb:
                while True:
                    coll = next(fff1)
                    line_num += 1
                    if "\t\t\t},\n" != coll:
                        # \t\t\t},\n가 나올 때까지 다음 줄을 계속 호출해 검사함.
                        if re.search("[가-힣]", coll):
                            save_txt.write(coll)
                            linenum_list.append(line_num)
                    else:
                        break
            # 선택지 문장 추출
            if "\t\t\t\tja = {\n" == bb or "\t\t\t\tja={\n" == bb:
                while True:
                    coll = next(fff1)
                    line_num += 1
                    if "\t\t\t\t},\n" != coll:
                        # \t\t\t},\n가 나올 때까지 다음 줄을 계속 호출해 검사함.
                        if re.search("[가-힣]", coll):
                            save_txt.write(coll)
                            linenum_list.append(line_num)
                    else:
                        break
            line_num += 1

    if save_dir2.stat().st_size == 0:  # 추출할 거리가 없어 비어있는 텍스트 파일 삭제.
        save_dir2.unlink()  # pathlib을 써서 파일 삭제.
    else:
        ext_dic[dir] = linenum_list
        # 추출한 파일 이름과 추출한 줄 위치값 저장.

with open("coordinate.pickle", "wb") as coordinate:
    # 추출한 원문의 위치값 저장용
    pickle.dump(ext_dic, coordinate)
