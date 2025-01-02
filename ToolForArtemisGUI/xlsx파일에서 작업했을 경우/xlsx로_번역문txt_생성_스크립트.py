import openpyxl
import pathlib
import re
from collections import deque
# ext_script폴더 생성하고 거기에 원문 넣기

# 비교할 텍스트 파일 경로
path_dir = pathlib.Path("ext_script/2장")

# 비교할 엑셀 파일의 경로
load_wb = openpyxl.load_workbook("유성월드액터2_2장.xlsx", data_only=True)


# 비교할 엑셀 파일의 시트 이름
load_ws = load_wb["시트1"]

# 변경한 텍스트 줄을 저장하는 리스트.
change_lines = []

# 선택지 떄문에 쓰는 작은 메모리.
save_memory = ()

# 원문 텍스트 파일 목록
path_dirs = path_dir.iterdir()
# 비교할 텍스트 파일 불러오기
current_file = next(path_dirs)
with open(current_file, "r", encoding="utf-8") as txt:
    iter_txts = iter(txt.readlines())

name_dic = {
    "シュバルト": "슈발트",
    "鮫郭": "사메카쿠",
    "ケーニッヒ": "쾨니히",
    "ストーカー": "스토커",
    "女の人": "여자",
    "ハールソン": "할슨",
    "大門寺": "다이몬지",
    "伊代": "이요",
    "メル": "멜",
    "女の声": "여자 목소리",
    "シフォン": "시폰",
    "武蔵": "무사시",
    "教団員Ｂ": "교단원B",
    "教団員Ａ": "교단원A",
    "門真": "카도마",
    "ベータ": "베타",
    "アルファ": "알파",
    "受付": "접수원",
    "マルゲッツィ": "마르게치",
    "手下": "부하",
    "吾郎": "고로",
    "情報屋": "정보상",
    "ナナシ": "나나시",
    "マスター": "마스터",
    "アレックス": "알렉스",
    "小町": "코마치",
    "？？？": "???",
    "男Ｃ": "남자C",
    "男２": "남자2",
    "男Ｂ": "남자B",
    "男Ａ": "남자A",
    "オッサン": "아저씨",
    "ハンズ": "핸즈",
    "ストライコス": "스트라이코스",
    "警官": "경관",
    "警官Ｇ": "경관G",
    "警官Ｅ": "경관E",
    "警官Ｄ": "경관D",
    "警官Ｃ": "경관C",
    "警官Ｂ": "경관B",
    "警官Ａ": "경관A",
    "警官Ｆ": "경관F",
    "女": "여자",
    "クライマー": "클라이머",
    "女性": "여성",
    "冬美": "후유미",
    "上層部B": "상층부B",
    "上層部A": "상층부A",
    "生田": "이쿠타",
    "メリッサ": "멜리사",
    "リンダ": "린다",
    "ルカ": "루카",
    "クラリス": "클라리스",
    "涼子": "료코",
    "ながれ": "나가레",
    "珠子": "타마코",
    "ヴァース": "버스",
    "係長": "계장",
    "宗助": "소스케",
    "ボーンズ": "본즈",
    "エルフ男": "엘프 남자",
    "男": "남자",
}
# 이름 사전, 변경할 이름을 추가하면 됨.
# 모든 행 단위로 출력
for row in load_ws.rows:
    # print(row)
    # print(row[0].value)
    if "원본" == row[0].value:
        continue

    # 비교할 텍스트 파일의 줄과 엑셀 파일의 줄이 일치하는지 검사
    try:
        text_line = next(iter_txts)
    except (
        StopIteration
    ):  # 텍스트 파일의 줄이 남아있지 않을 경우 저장하고 다음 텍스트 파일을 불러옴.
        print(
            "텍스트 파일의 줄이 남아있지 않습니다.\n번역문을 삽입한 파일을 저장하고 다음 텍스트 파일을 불러옵니다."
        )
        with open(
            "save_script/" + current_file.name, "w", encoding="utf-8"
        ) as save_script:
            save_script.writelines(change_lines)

        # 저장하고 초기화.
        change_lines = []

        try:
            current_file = next(path_dirs)
        except StopIteration:  # 모든 텍스트 파일을 비교했을 경우 종료.
            print("모든 텍스트 파일을 비교했습니다. 종료합니다.")
            quit()

        with open(current_file, "r", encoding="utf-8") as txt:
            iter_txts = iter(txt.readlines())
        text_line = next(iter_txts)

    # text=가 없을 경우 - 선택지가 뜰 때, 텍스트창에 적히는 문장을 의미.
    if re.match('\t\t\t\t"', text_line):
        compare_line = re.search('(?<=").+?(?=")', text_line).group()
        if row[0].value == compare_line:
            change_line = text_line.replace(compare_line, row[2].value)
            change_lines.append(change_line)
            continue
        else:
            print("일치하지 않음")
            print(current_file.name)
            print(row[0].value)
            print(compare_line)
            quit()

    if re.match("\t\t\t\ttext=", text_line):
        print("선택지일 때, 텍스트창 안의 텍스트입니다")
        compare_line = re.search('(?<=").+?(?=")', text_line).group()
        print(save_memory)
        if save_memory[0] == compare_line:
            print("일치함")
            print(text_line)
            change_line = text_line.replace(compare_line, save_memory[1])
            print(change_line)
            change_lines.append(change_line)
            text_line = next(iter_txts)

        else:
            print("일치하지 않음")
            print(current_file.name)
            print(row[0].value)
            print(compare_line)
            quit()

    # 스크립트 파일에 ruby가 있을 경우, 요미가나. - 그냥 text=부분만 비우기.
    if '"ruby"' in text_line:
        print("루비 있음")
        compare_ruby = re.search('(?<=text=").+?(?=")', text_line).group()
        print(compare_ruby)
        text_line = text_line.replace(compare_ruby, "")
        print(text_line)
        change_lines.append(text_line)
        # 루비가 있는 줄을 건너뛰기 위해 다음 줄을 호출함.
        text_line = next(iter_txts)

    # 스크립트 파일에 이름 표기가 있을 경우 - 따로 빼서 이름만 교체하기.
    if "name = " in text_line:
        compare_names = re.findall('(?<=")[^,]+?(?=")', text_line)
        print(compare_names)
        for name in compare_names:
            if name_dic.get(name):
                # print("이름 있음")
                text_line = text_line.replace(name, name_dic.get(name))

            else:
                print("이름 없음")
                print(name)
                print(text_line)
                quit()

        print(text_line)
        change_lines.append(text_line)
        # 이름이 있는 줄을 건너뛰기 위해 다음 줄을 호출함.
        text_line = next(iter_txts)

    compare_line = re.search('(?<=").+?(?=")', text_line).group()
    # 		 "「相手を見てモノを言えよ」", -> 「相手を見てモノを言えよ」
    if row[0].value == compare_line:
        # print("일치함")
        save_memory = (
            compare_line,
            row[2].value,
        )  # 선택지 창에 뜨는 텍스트를 저장하기 위한 용도.
        print(text_line)
        change_line = text_line.replace(compare_line, row[2].value)
        print(change_line)
        change_lines.append(change_line)

        continue
    else:
        print("일치하지 않음")
        print(current_file.name)
        print(row[0].value)
        print(compare_line)
        quit()
