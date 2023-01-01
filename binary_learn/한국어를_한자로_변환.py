import binascii

a = open("tbl_chs.txt", "r", encoding="utf-16")
a1 = a.readlines()
a.close()
d = {}  # 한자 변환용 딕셔너리
for a2 in a1:
    b = binascii.unhexlify(a2[0:4])
    c = a2[5]
    d[c] = b

korea = "이쪽을 수정하면 됨"
trans = bytearray()

for k in korea:
    try:
        trans = trans + d[k]
    except KeyError:
        trans = trans + k.encode("cp932", errors="ignore")
        pass

print(korea.encode("cp949", errors="ignore").hex())  # 한국어 인코딩으로 표현되는 헥스값
print(trans.decode("cp932"))  # 한문으로 변환된 한국어
print(trans.hex())  # 일본어 인코딩으로 표현되는 헥스값
