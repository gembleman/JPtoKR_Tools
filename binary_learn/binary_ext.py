import os
import binascii
import re

path_dir = "원본dat"
save_dir = "추출완료"
file_list = os.listdir(path_dir)


# 일본어 문자열 헥스 사전을 불러와서 대조해보면 되잖아.
open1 = open("일본어감지사전.txt", "r", encoding="utf-16")
open12 = open1.readlines()
open1.close()
dic = set()
dic2 = set()  # 영어 저장용
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


def main(ans):
    def search(num):
        init1 = num
        while True:
            num += 2
            cola4 = bytes(a1[num : num + 2])
            if cola4 not in dic:
                break
        jj.write(a1[init1:num].decode("cp932") + "\n")
        for x in range(
            init1, num - 1
        ):  # 왜 num에다 -1을 해야 되나, 문자열 길이에서 하나를 빼줘야 커서 위치와 aaa값이 정확히 맞아떨어짐.
            # 예를 들어 1,2,3이런 목록이 있을 때, 문자열 길이가 3이니 세번 건너뛰어야 겠다 하고 next를 세번 쓰면 2, 3, ? 가 빠짐. 1은 이미 빠져있음. for문으로 1을 aaa로 불러왔잖아.
            next(cola1)

        return num

    if ans not in ["1", "2", "3"]:  # 예외 처리
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

        if ans == "2":  # 아스키코드 추출하는 줄
            file_name = save_dir + "//" + li + "_shift-jis.txt"
            lll = open(file_name, "w", encoding="cp932")
            num11 = 0
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

                    cc = a1[num_int:num11].decode("cp932")
                    if len(cc) > 1:  # \x61 이렇게 1바이트 크기로 추출되는 건 제외.
                        lll.write(cc + "\n")
                else:
                    num11 += 1
            lll.close()
            if os.stat(file_name).st_size == 0:  # 빈 텍스트 파일 삭제.
                print("추출된 아스키코드가 없습니다.")
                os.remove(file_name)

        if ans == "1":  # 일본어 문자열 추출
            file_name = save_dir + "//" + li + ".txt"
            jj = open(file_name, "w", encoding="utf-8")
            for aaa in cola1:
                # 세 칸을 두 칸씩 나눠서 검사. 결과에 따라 이동량이 달라짐.
                cola2 = bytes(a1[num : num + 2])
                cola3 = bytes(a1[num + 1 : num + 3])

                if cola2 in dic:  # 앞 부분에 일본어가 있는 경우
                    # print("search 하기 전:" + str(num))
                    # 두 칸씩 계속 뒷부분을, 가능할 때까지 검사한다.
                    num = search(num)
                    # print("cola2 :" + str(num))
                    continue

                else:
                    if cola3 in dic:  # 뒤에 있는 부분에 일본어가 있는 경우
                        # 두칸씩 계속 뒷부분을 검사
                        next(cola1)  # 커서 한 칸 옮김
                        num += 1  # 커서 한 칸 옮김
                        num = search(num)
                        # print("cola3 :" + str(num))
                        continue
                    else:  # 둘 다 없는 경우
                        # 이때, 마지막 비트 그러니까 \x8F\xE3\x82에 \x82가 일본어 문자코드에 속하는 값인지 검사해야 함. \x82 다음에 등장하는 값이 \xd6일 경우 \x82\xd6은 일본어라 그 점도 고려해야 함..
                        # 그렇기 때문에 세칸씩 건너뛰는 게 아니라, 두칸씩 건너뜀.
                        try:
                            # print("커서:" + str(num))
                            # print(str(bytes([aaa])))
                            next(cola1)
                        except StopIteration:
                            print(str(bytes([aaa])))
                            print("추출 끝" + str(num))
                            break
                        num += 2
                        continue
                # next() 이게 핵심. - 리스트에서 추출한 요소들을 반복문으로 불러오지 않고 건너뛰게 한다.
                # 예를 들어 \xf0\xf0\xf0\xf0\xf0 이런 목록이 있다. 여기에 \xf0을 감지해 \xf0가 어디까지 반복되고 있는지 계산하고 추출하는 반복문이 있다면
                # 반복문이 한 번 추출했으면 \xf0 다음에 오는 또다른 \xf0을 불러오지 않고 건너뛰게 하는 방법이 필요하다.
            jj.close()
            if os.stat(file_name).st_size == 0:  # 빈 텍스트 파일 삭제.
                print("추출된 문장이 없습니다.")
                os.remove(file_name)

        if ans == "3":  # 헥스값 추출
            file_name2 = save_dir + "//" + li + "_hex.txt"
            jj2 = open(file_name2, "wb")  # 헥스값으로 보는 용
            for aaa in cola4:
                if hex(aaa) not in dic3:  # 안쓰이는 헥스값을 제외하고 전부 추출
                    num2 = num
                    while True:
                        num2 += 1  # 다음 헥스값을 호출하기 위해
                        a45 = hex(a1[num2])
                        if a45 in dic3:
                            break

                    if len(a1[num:num2]) == 1:  # 바이트 하나 크기로 걸러진 건 추출하지 않음.
                        num += 1
                        continue

                    jj2.write(a1[num:num2])
                    for x in range(num2 - num - 1):  # 하나 더 빼줘야 커서 위치가 정확하게 옮겨짐.
                        num += 1
                        next(cola4)

                    num += 1
                    continue

                else:
                    num += 1
            jj2.close()
            if os.stat(file_name2).st_size == 0:  # 빈 텍스트 파일 삭제.
                print("추출된 문장이 없습니다.")
                os.remove(file_name2)


# 기능을 두 개 만들어야겠음.
# 하나는 일본어와 함께 아스키 코드, 반각 가타카나도 추출해주는 기능.
# 또 하나는 일본어만 추출해주는 기능.
# 3번 헥스 값 추출 기능 추가함.

if __name__ == "__main__":
    ans = input("1번 일본어만 추출, 2번 아스키코드 추출, 3번 헥스값 추출// 1번 권장 : ")
    main(ans)
