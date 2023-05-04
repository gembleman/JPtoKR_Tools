from ctypes import WinDLL, c_char_p, c_int, c_wchar_p
from ctypes.wintypes import BOOL

import pathlib
import multiprocessing
import time
import sys


class TransEngine:
    def initialize(self, engine):
        self.start = engine.J2K_InitializeEx  # 얘가 함수
        self.start.argtypes = [c_char_p, c_char_p]
        self.start.restype = BOOL

        self.trans = engine.J2K_TranslateMMNTW  # 얘도 함수
        self.trans.argtypes = [c_int, c_wchar_p]
        self.trans.restype = c_wchar_p

        self.start_obj = self.start(b"CSUSER123455", b"C:\Program Files (x86)\ChangShinSoft\ezTrans XP\Dat")

    def translate_j2k(self, src_text):  # 단문 번역 메소드 - 한번에 번역할 수 있는 텍스트 길이는 4기가 정도로 추정. 대신 그만큼 느려짐.
        trans_obj = self.trans(0, src_text)
        return trans_obj

    def main(self, a22):  # 텍스트 파일들 번역용, 텍스트 파일 목록만 전달 받도록 함.
        a22 = pathlib.Path(a22)
        if a22.is_file():  # 파일을 넣었을 시
            a23 = a22.parent / "번역한_텍스트"
            a23.mkdir(exist_ok=True)
            a24 = [a22]
        elif a22.is_dir():  # 폴더를 넣었을 시
            a23 = a22 / "번역한_텍스트"
            a23.mkdir(exist_ok=True)
            a24 = list(a22.glob("**/*.txt"))
        start_time = time.perf_counter()
        with multiprocessing.Pool() as pool:
            for a1 in a24:
                # 텍스트 번역
                # 개별 버전에서는 추출이란 문자가 들어가 있지 않아도 번역이 되도록
                # pathlib에서 glob은 재귀적인 처리를 할 수 있게 해줌. 반복자로 값을 만들기 때문에 리스트로 변환.
                print(str(a1))

                with open(a1, "r", encoding="utf-8") as b:
                    bb = b.readlines()
                # bb = ["|:_"+b1 for b1 in bb]#리스트 컴프리헨션을 쓰고 싶으면 이렇게.

                for num, b1 in enumerate(bb):
                    b1 = "|:_" + b1
                    bb[num] = b1  # 이터레이터를 써서 메모리 낭비를 줄이면 어떨까.

                aaa = pool.map(local_trans, bb)

                for num, aaa1 in enumerate(aaa):
                    aaa1 = aaa1.replace("|:_", "")
                    aaa[num] = aaa1

                # aaa = [aaa1.replace("|:_","") for aaa1 in aaa]
                file_path = a23 / a1.stem
                with open(str(file_path) + "_번역.txt", "w", encoding="utf-8-sig") as c:
                    c.writelines(aaa)

        end_time = time.perf_counter()
        print(f"번역에 든 시간 : {int(round((end_time - start_time) * 1000))}ms")


try:
    engine_object = WinDLL(r"C:\Program Files (x86)\ChangShinSoft\ezTrans XP\J2KEngine.dll")
except Exception as e:
    print(e)
    print("이지트랜스 설치 경로는 반드시 C:\Program Files (x86)\ChangShinSoft\ezTrans XP\가 돼야 합니다.")
    input()  # 코드 정지용
    sys.exit()

eng = TransEngine()
eng.initialize(engine_object)


def local_trans(text):
    return eng.translate_j2k(text)


# 파이썬 32비트 버전에서만 됩니다. - 이 때문에 64비트 파이썬에서 쓰려면 exe를 만들어 외부로 빼야할 듯.
# 출처
# https://github.com/HelloKS/ezTransWeb


if __name__ == "__main__":
    multiprocessing.freeze_support()
    print("Qootrans ver.0.3 !@!번역하려는 텍스트는 utf-8으로 인코딩되었고, .txt 확장자를 가진 텍스트여야 합니다!@!")
    # print("qoo_call")
    # print(sys.argv)
    # start = time.time()
    # plag = 0
    pp = None
    if len(sys.argv) == 1:
        # 인자가 없으면 실행됨.
        print("call_eztrans file_mode (원문 폴더 경로) <-이런 식으로 입력")
        eng.main(r"C:\Users\nsoop\Desktop\workingfolder_current\JPtoKR_Tools\Qootranslator\GUI.ver\새 폴더")  # 번역에 든 시간 : 15557ms - 15.5초
        input()  # 코드 정지용
        sys.exit()

    else:
        # 인자가 있으면 실행.

        if sys.argv[1] == "clip_mode":
            input_com = sys.argv[2]
            while input_com != "exit":
                print(local_trans(input_com))
                input_com = input()
        elif sys.argv[1] == "file_mode":
            eng.main(sys.argv[2])

            # queue를 이용해 반환값을 방출하기.
        else:
            print("인자가 잘못되었습니다.")
            input()  # 코드 정지용
            sys.exit()

    # 테스트해보니, 몇백개의 텍스트 파일을 작업하는 데 시간이 더럽게 오래걸림.
    # 병렬처리로 만들어야겠음. - 긴가민가했지만, 멀티쓰레드가 안 됨. 멀티프로세스로 시도.
    # enhd 적용 확인. - 그러나 때때로 적용이 안되는 경우가 있음. 원인을 모르겠다.
    # 버그 1 - 문자열 맨 앞에 전각 공백'　', 그냥 공백' '이 있는 경우 알아서 생략이 되서 출력. - 문자열 중간에 공백이 있어도 마찬가지.
    # 버그 2 - 때때로 ehnd가 이상하게 적용되는 경우가 있음. - |:_  넣어서 해결.
    # 리스트 컴프리헨션을 쓴 경우 - 번역에 든 시간 : 0:00:51.382579
    # 그냥 for문 쓴 경우 - 번역에 든 시간 : 0:00:51.369040
    # 다 때려치고 for문만 주구장창 쓰는 거로.
