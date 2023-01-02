import os
import binascii

a6 = open("tbl_chs.txt", "r", encoding="utf-16")  # tbl_chs.txt는 한글 폰트 출력에 필요한 매칭사전.
a61 = a6.readlines()
a6.close()
dic1 = {}  # 한자 변환용 딕셔너리
for a2 in a61:
    b = binascii.unhexlify(a2[0:4])
    c = a2[5]
    dic1[c] = b


def trans1(korea):  # korea는 들어올 번역문
    trans = bytearray()

    for k in korea:
        try:
            trans = trans + dic1[k]
        except KeyError:
            trans = trans + k.encode("cp932", errors="ignore")
            pass
        # trans에는 헥스로 변환된 값이 들어있음.

    return trans


dic = [
    "0x10",
    "0x11",
    "0x12",
    "0x13",
    "0x14",
    "0x15",
    "0x16",
    "0x17",
    "0x18",
    "0x1a",
    "0x1c",
    "0xb6",
    "0x0",
    "0x2",
    "0xff",
    "0x1",
    "0x4",
    "0x3",
    "0x5",
    "0xfe",
    "0x6",
    "0x7",
    "0x8",
    "0xf",
    "0xd",
    "0xa",
    "0xb",
    "0xc",
    "0xd",
    "0xe",
    "0x80",
]
path_dir = "원본dat"
read_dir = "추출완료"
save_dir = "저장"
file_list = os.listdir(read_dir)

for li in file_list:
    if "_번역.txt" in li:
        print(li)
        a = open(path_dir + "//" + li[0:-7], "rb")  # 불러올 바이너리 파일
        a1 = bytearray(a.read())
        a.close()
        u = open(read_dir + "//" + li, "r", encoding="utf-8-sig")  # 불러올 번역한 파일
        u2 = u.readlines()
        u.close()
        number_con = 0  # 번역한 파일 불러올 때 쓸 문장 번호
        ext_list = bytearray()

        cola1 = iter(a1)  # 이게 핵심. - 리스트에서 추출한 요소들을 반복문으로 불러오지 않고 건너뛰게 한다.
        num = 0  # 문자 위치가 저장되는 변수

        for aaa in cola1:

            a34 = hex(aaa)
            if a34 not in dic:
                flag = None
                num2 = num
                while True:
                    num2 += 1  # 다음 헥스값을 호출하기 위해
                    a45 = hex(a1[num2])
                    if a45 in dic:
                        break

                if len(a1[num:num2]) == 1:  # 바이트 하나 크기로 걸러진 건 수집하지 않음.
                    ext_list += bytes([aaa])
                    num += 1
                    continue

                u33 = u2[number_con].replace("\n", "")
                number_con += 1  # 하나 카운트

                b22 = a1[num:num2]

                if u33 != b22:
                    b22 = trans1(u33)  # 바이트로 저장
                ext_list += b22

                for x in range(num2 - num - 1):  # 하나 더 빼줘야 커서 위치가 정확하게 옮겨짐.
                    num += 1
                    next(cola1)
                    # 이게 핵심. - 리스트에서 추출한 요소들을 반복문으로 불러오지 않고 건너뛰게 한다.
                    # 예를 들어 리스트에서 \xf0을 감지해 \xf0가 어디까지 반복되고 있는지 계산하고 추출하는 반복문이 있다면
                    # 반복문이 한 번 추출했으면 \xf0 다음에 오는 또다른 \xf0을 불러오지 않고 건너뛰게 하는 방법이 필요하다.

                num += 1
                continue

            else:
                ext_list += bytes([aaa])
                num += 1

        file_name2 = save_dir + "//" + li[0:-7]
        jj2 = open(file_name2, "wb")  # 헥스값으로 보는 용
        jj2.write(ext_list)
        jj2.close()

# system.dat 파일은 직접 수정해야됨.
