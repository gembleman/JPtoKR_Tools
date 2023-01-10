import os
import binascii
import re

a6 = open("변환용한자표.txt", "r", encoding="utf-16")  # 변환용한자표.txt는 한글 폰트 출력에 필요한 매칭사전.
a61 = a6.readlines()
a6.close()
korea_dic1 = {}  # 한자 변환용 딕셔너리
for a2 in a61:
    ccc = re.search("^.+?(?=\=)", a2)
    ccc2 = re.search("(?<=\=).", a2)
    if (ccc != None) and (ccc2 != None):
        b = binascii.unhexlify(ccc.group())
        korea_dic1[ccc2.group()] = b


def trans1(korea):  # korea는 들어올 번역문
    trans = bytearray()

    for k in korea:
        try:
            trans = trans + korea_dic1[k]
        except KeyError:
            try:
                trans = trans + k.encode("cp932")
            except Exception as inst:
                print(inst)
                quit()
            pass
        # trans에는 헥스로 변환된 값이 들어있음.

    return trans


# 일본어 문자열 헥스 사전을 불러와서 대조해보면 되잖아.
open1 = open("일본어감지사전.txt", "r", encoding="utf-16")
open12 = open1.readlines()
open1.close()
dic = set()
dic2 = set()  # 영어, 아스키코드 저장용
for a2 in open12:
    # 헥스가 4개인 줄, 2개인 줄 따로 나눠서 사전 만들기.
    ccc = re.search("^.+?(?=\=)", a2)
    if ccc != None:
        b = binascii.unhexlify(ccc.group())
        if len(ccc.group()) == 2:
            dic2.add(b)
            continue
        if len(ccc.group()) == 4:
            dic.add(b)
            continue

        print("이상한 줄:" + a2)
        quit()
    else:
        print("에러")
        quit()

dic3 = [  # 이 값들은 절대 일본어 문자열을 표현하는 데 쓰이는 헥스값이 아님.
    "0x0",
    "0x1",
    "0x2",
    "0x3",
    "0x4",
    "0x5",
    "0x6",
    "0x7",
    "0x8",
    "0x9",
    "0xa",
    "0xb",
    "0xc",
    "0xd",
    "0xe",
    "0xf",
    "0x10",
    "0x11",
    "0x12",
    "0x13",
    "0x14",
    "0x15",
    "0x16",
    "0x17",
    "0x18",
    "0x19",
    "0x1a",
    "0x1b",
    "0x1c",
    "0x1d",
    "0x1e",
    "0x1f",
    "0xfd",
    "0xfe",
    "0xff",
    "0x7f",
]

path_dir = "원본파일"
save_dir = "추출완료"
file_list = os.listdir(path_dir)


def main(ans):
    def search(num, n):
        init1 = num
        flag = 0
        while True:
            num += 2
            cola4 = bytes(a1[num : num + 2])
            if cola4 not in dic:
                black_list = [
                    b"\x2e\x73\x70\x6d",
                    b"\x2e\x6f\x67\x67",
                ]
                if bytes(a1[num : num + 4]) in black_list:  # .spm 확장자일 경우 기록하지 않음.
                    flag = 1
                break
        if flag == 1:
            jj.write(a1[init1:num])
        if flag == 0:
            kkk = bun2[n].replace("\n", "")
            sentense = trans1(kkk)
            jj.write(sentense)
            n += 1
        for x in range(
            init1, num - 1
        ):  # 왜 num에다 -1을 해야 되나, 문자열 길이에서 하나를 빼줘야 커서 위치와 aaa값이 정확히 맞아떨어짐.
            # 예를 들어 1,2,3이런 목록이 있을 때, 문자열 길이가 3이니 세번 건너뛰어야 겠다 하고 next를 세번 쓰면 2, 3, ? 가 빠짐. 1은 이미 빠져있음. for문으로 1을 aaa로 불러왔잖아.
            next(cola1)

        return num, n

    if ans not in ["1", "2", "3"]:  # 입력 예외 처리
        print("잘못된 입력")
        quit()

    for li in file_list:
        print(li)
        a = open(path_dir + "//" + li, "rb")  # 불러올 바이너리 파일
        a1 = bytearray(a.read())
        a.close()

        cola1 = iter(a1)  # 이게 핵심. - 리스트에서 추출한 요소들을 반복문으로 불러오지 않고 건너뛰게 한다.
        cola2 = iter(a1)
        cola4 = iter(a1)
        num = 0  # 문자 위치가 저장되는 변수

        print(len(a1))

        if ans == "1":  # 번역한 일본어 문자열 삽입
            save_dir = "문자열_추출"
            file_name = save_dir + "//" + li + "_번역.txt"
            if os.path.isfile(file_name) == False:
                print("삽입할 파일 없음 넘어감")
                continue
            bun1 = open(file_name, "r", encoding="utf-8-sig")
            bun2 = bun1.readlines()
            bun1.close()
            name55 = "번역한_문자열_삽입됨"
            if not os.path.exists(name55):  # 폴더 없으면 만드는 줄
                os.makedirs(name55)
            jj = open(name55 + "//" + li, "wb")
            sentence_num = 0  # 삽입할 문자열 리스트 순서
            for aaa in cola1:
                # 세 칸을 두 칸씩 나눠서 검사. 결과에 따라 이동량이 달라짐.
                coloo2 = bytes(a1[num : num + 2])
                coloo3 = bytes(a1[num + 1 : num + 3])

                if coloo2 in dic:  # 앞 부분에 일본어가 있는 경우
                    # print("search 하기 전:" + str(num))
                    # 두 칸씩 계속 뒷부분을, 가능할 때까지 검사한다.
                    num, sentence_num = search(num, sentence_num)
                    # print("cola2 :" + str(num))
                    continue

                else:
                    if coloo3 in dic:  # 뒤에 있는 부분에 일본어가 있는 경우
                        # 두칸씩 계속 뒷부분을 검사
                        jj.write(bytes([a1[num]]))
                        next(cola1)  # 커서 한 칸 옮김
                        num += 1  # 커서 한 칸 옮김
                        num, sentence_num = search(num, sentence_num)
                        # print("cola3 :" + str(num))
                        continue
                    else:  # 둘 다 없는 경우
                        # 이때, 마지막 비트 그러니까 \x8F\xE3\x82에 \x82가 일본어 문자코드에 속하는 값인지 검사해야 함. \x82 다음에 등장하는 값이 \xd6일 경우 \x82\xd6은 일본어라 그 점도 고려해야 함..
                        # 그렇기 때문에 세칸씩 건너뛰는 게 아니라, 두칸씩 건너뜀.
                        jj.write(coloo2)
                        try:
                            # print("커서:" + str(num))
                            # print(str(bytes([aaa])))
                            next(cola1)
                        except StopIteration:
                            print(str(bytes([aaa])))
                            print("추출 끝" + str(num))
                            break
                        num += 2

                # next() 이게 핵심. - 리스트에서 추출한 요소들을 반복문으로 불러오지 않고 건너뛰게 한다.
                # 예를 들어 \xf0\xf0\xf0\xf0\xf0 이런 목록이 있다. 여기에 \xf0을 감지해 \xf0가 어디까지 반복되고 있는지 계산하고 추출하는 반복문이 있다면
                # 반복문이 한 번 추출했으면 \xf0 다음에 오는 또다른 \xf0을 불러오지 않고 건너뛰게 하는 방법이 필요하다.
            jj.close()

        if ans == "2":  # 번역한 시스템문자열(아스키코드) 삽입하는 줄 - 구현함
            save_dir = "시스템_문자열_추출"
            file_name2 = save_dir + "//" + li + "_sys.txt"
            if os.path.isfile(file_name2) == False:
                print("삽입할 파일 없음 넘어감")
                continue
            name55 = "시스템_문자열_삽입됨"
            if not os.path.exists(name55):  # 폴더 없으면 만드는 줄
                os.makedirs(name55)
            file_name = name55 + "//" + li
            jj3 = open(file_name, "wb")
            lll2 = open(file_name2, "r", encoding="cp932")
            lll3 = lll2.readlines()
            lll2.close()
            num11 = 0
            line_jump = 0
            for aaa in cola2:
                # print(bytes([aaa]))
                # print(num11)
                if bytes([aaa]) in dic2:
                    num_int = num11
                    while True:
                        num11 += 1
                        if bytes([a1[num11]]) not in dic2:
                            break
                        next(cola2)

                    cc = a1[num_int:num11]
                    if len(cc) > 1:  # 다 저장.
                        lll4 = lll3[line_jump].replace("\n", "")
                        jj3.write(lll4.encode("cp932"))
                        line_jump += 1
                    else:
                        jj3.write(cc)
                else:
                    jj3.write(bytes([aaa]))
                    num11 += 1
            jj3.close()

        if ans == "3":
            # 번역한 헥스값 삽입 - 구현 끝. - 헥스값 길이가 달라질 경우, 제대로 넣지 못함. - \xff를 구분자로 넣어야 할 듯 - 구현함.
            name55 = "헥스값_삽입됨"
            if not os.path.exists(name55):  # 폴더 없으면 만드는 줄
                os.makedirs(name55)
            save_dir = "헥스값_추출"
            file_name2 = save_dir + "//" + li + "_hex.txt"
            if os.path.isfile(file_name2) == False:
                print("삽입할 파일 없음 넘어감")
                continue
            file_name3 = name55 + "//" + li

            jj2 = open(file_name2, "rb")  # 헥스값으로 보는 용
            jj22 = bytearray(jj2.read())

            def kuhy(x):
                if bytes([jj22[x]]) == b"\xff":
                    return x
                else:
                    return None

            FF_location = list(filter(kuhy, range(len(jj22))))  # 0xff의 위치리스트
            # print("0xff의 위치")
            # print(FF_location)
            print("삽입할 헥스값을, 리스트로 만드는 중")
            listnum = 0
            listnum2 = 0
            insert_list = []
            for x in range(len(FF_location)):
                insert_list.append(jj22[listnum : FF_location[listnum2]])
                listnum = FF_location[listnum2] + 1
                listnum2 += 1

            jj3 = open(file_name3, "wb")

            number = 0  # 추출한 바이너리 파일 읽어들일 때 쓸 용도
            for aaa in cola4:
                if hex(aaa) not in dic3:  # 안쓰이는 헥스값을 제외하고 전부 추출
                    num2 = num
                    while True:
                        num2 += 1  # 다음 헥스값을 호출하기 위해
                        a45 = hex(a1[num2])
                        if a45 in dic3:
                            break

                    if len(a1[num:num2]) == 1:  # 바이트 하나 크기로 걸러진 것도 삽입.
                        jj3.write(bytes([aaa]))
                        num += 1
                        continue

                    jj3.write(insert_list[number])
                    for x in range(num2 - num - 1):  # 하나 더 빼줘야 커서 위치가 정확하게 옮겨짐.
                        num += 1
                        next(cola4)

                    num += 1
                    number += 1
                    continue

                else:
                    jj3.write(bytes([aaa]))
                    num += 1
            jj2.close()


# 기능을 두 개 만들어야겠음.
# 하나는 일본어와 함께 아스키 코드, 반각 가타카나도 추출해주는 기능.
# 또 하나는 일본어만 추출해주는 기능.
# 3번 헥스 값 추출 기능 추가함.

if __name__ == "__main__":
    ans = input(
        "1번 번역된 일본어 문자열을 삽입, 2번 번역된 시스템문자열(아스키코드)을 삽입, 3번 번역된 헥스값을 삽입// 1번 권장 : "
    )
    main(ans)
    
# system.dat 파일은 직접 수정해야됨.
