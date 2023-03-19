from pathlib import Path
import pickle

trans_dir = Path("ext_script/번역한_텍스트")
save_dir = Path("chaged_script")
save_dir.mkdir(exist_ok=True)  # 저장할 폴더 생성.

with open("coordinate.pickle", "rb") as fr:
    ext_dic = pickle.load(fr)

for ext_dir in ext_dic.keys():
    # script 폴더의 파일 목록은 검색하지 않는다. pickle파일에 교체해야될 스크립트 파일 목록이 담겨있으니까 그걸 쓰면 된다.
    print(ext_dir)
    with open(ext_dir, "r", encoding="utf-8") as ext_file:
        ext_lines = ext_file.readlines()
    trans_dir2 = trans_dir / Path(Path(ext_dir).stem + "_번역.txt")
    with open(trans_dir2, "r", encoding="utf-8-sig") as trans_file:
        trans_lines = trans_file.readlines()
    trans_nums = ext_dic[ext_dir]
    # 번역문을 원본 스크립트에 삽입.
    for trans_num, trans_line in zip(trans_nums, trans_lines):
        ext_lines[trans_num] = trans_line

    # 교체한 스크립트 저장.
    save_dir2 = save_dir / Path(ext_dir).name
    with open(save_dir2, "w", encoding="utf-8") as save:
        save.writelines(ext_lines)
