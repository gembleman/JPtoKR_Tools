a = open("button.dat", "rb")  # 불러올 바이너리 파일
a1 = bytearray(a.read())

ext_list = []
dic = [
    "0x0",
    "0x2",
    "0xff",
    "0x1",
    "0x4",
    "0xd2",
    "0x3",
    "0x14",
    "0x5",
    "0xfe",
    "0x6",
    "0x7",
]

cola1 = iter(a1)  # 이게 핵심. - 리스트에서 추출한 요소들을 반복문으로 불러오지 않고 건너뛰게 한다.
num = 0  # 문자 위치가 저장되는 변수

for aaa in cola1:

    a34 = hex(aaa)
    # print(a34)
    if a34 not in dic:
        flag = None
        num2 = num
        while True:
            num2 += 1  # 다음 헥스값을 호출하기 위해
            a45 = hex(a1[num2])
            if a45 not in dic:
                flag = 2
            else:  # 다음에 0이나 FF가 오는 경우
                if num == num2 - 1:  # 바로 다음에 0이나FF가 온다는 소리니까. 그런 건 걸러낸다.
                    flag = 1
                break

        if flag == 2:
            print("num:" + str(num) + "num2:" + str(num2))
            b2 = a1[num:num2]
            print(b2)

            ext_list.append(b2)
            num3 = num2 - num
            print("이만큼 커서를 건너뜁니다 : " + str(num3))
            for x in range(num3):
                num += 1
                next(cola1)
                # 이게 핵심. - 리스트에서 추출한 요소들을 반복문으로 불러오지 않고 건너뛰게 한다.
                # 예를 들어 리스트에서 \xf0을 감지해 \xf0가 어디까지 반복되고 있는지 계산하고 추출하는 반복문이 있다면
                # 반복문이 한 번 추출했으면 \xf0 다음에 오는 또다른 \xf0을 불러오지 않고 건너뛰게 하는 방법이 필요하다.

        if flag == 1:
            num += 1
            continue  # 다음으로 넘어감.

    num += 1

jj = open("werds.txt", "w", encoding="utf-8")
jj2 = open("werds_binary.txt", "wb")  # 헥스값으로 보는 용
for eee in ext_list:
    e3 = eee.decode("cp932", errors="ignore")  # cp932로 문자열 해독
    jj.write(e3 + "\n")  # utf-8로 다시 인코딩되어 기록됨.
    jj2.write(eee)
