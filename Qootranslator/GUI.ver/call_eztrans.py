from ctypes import WinDLL, c_char_p, c_int, c_wchar_p
from ctypes.wintypes import BOOL

import pathlib
import concurrent.futures
import time
import sys


class TransEngine:
    def initialize(self, engine):
        start = engine.J2K_InitializeEx  # 얘가 함수
        start.argtypes, start.restype = (c_char_p, c_char_p), BOOL

        trans = engine.J2K_TranslateMMNTW  # 얘도 함수
        trans.argtypes, trans.restype = (c_int, c_wchar_p), c_wchar_p
        self.trans = trans

        self.start_obj = start(b"CSUSER123455", b"C:\Program Files (x86)\ChangShinSoft\ezTrans XP\Dat")


try:
    engine_object = WinDLL(r"C:\Program Files (x86)\ChangShinSoft\ezTrans XP\J2KEngine.dll")
except Exception as e:
    print(str(e).join("\n이지트랜스 설치 경로는 반드시 C:\Program Files (x86)\ChangShinSoft\ezTrans XP\가 돼야 합니다."))
    input()  # 코드 정지용
    sys.exit()

eng = TransEngine()
eng.initialize(engine_object)


def clip_trans(text):  # 클립보드 번역용
    try:
        a = eng.trans(0, "".join(["|:_", text])).lstrip("|:_")
    except Exception as e:
        print(e)

    return a


def main(a22):  # 텍스트 파일들 번역용, 텍스트 파일 목록만 전달 받도록 함.
    path = pathlib.Path(a22)
    a23 = (path.parent.joinpath("번역한_텍스트"), path.joinpath("번역한_텍스트"))
    if path.is_file():  # 파일을 넣었을 시
        a24, save_path1 = (path,), a23[0]
        save_path1.mkdir(exist_ok=True)
    else:  # 폴더를 넣었을 시
        a24, save_path1 = (path.glob("**/*.txt")), a23[1]
        try:
            save_path1.mkdir()
        except FileExistsError:
            flag = input("번역한 텍스트가 이미 있는 것 같습니다. 덮어쓰시겠습니까? (y/n) :")
            if flag == "y":
                a24 = [s for s in a24 if "\\번역한_텍스트\\" not in str(s)]
            else:
                sys.exit()
    start_time = time.perf_counter()

    # 리스트 컴프리헨션을 세 개 써서 해결하는 방법.
    # a24 = [s for s in a24 if "\\번역한_텍스트\\" not in s]

    # aaa2 = []
    # self.nn = 0
    # map1 = executor.map()
    # wait1 = concurrent.futures.wait()
    # submit1 = executor.submit()
    """
    def rotaion_file(la_text):  # 이중 맵
        return executor.map(clip_trans, la_text, chunksize=2048)
    """

    def readfile(txt_path):
        with open(txt_path, "r", encoding="utf-8") as f:
            return f.readlines()

    def writefile(file_path, text_list2):
        with open("".join([str(save_path1 / file_path.stem), "_번역.txt"]), "w", encoding="utf-8") as f:
            f.writelines(text_list2)
        return 1

    text_list = []
    trans_texts = []
    ll = []
    # large_texts = [thread.submit(readfile, i) for i in a24]
    with concurrent.futures.ThreadPoolExecutor() as thread:
        for large_texts in thread.map(readfile, a24):  # 멀티쓰레드를 사용하여 파일 입출력을 빠르게 함.
            text_list.append(large_texts)
    print("파일 읽기 완료")
    print(type(text_list))
    print(type(text_list[0]))
    aaa = list(text_list[0])
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    # for file_path, tl in zip(a24, text_list):
    # max_workers=12
    # 텍스트 줄 수에 따라 프로세스 수를 조절하는 게 좋을 듯.
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    # app = executor.map(clip_trans, tl)
    # concurrent.futures.ProcessPoolExecutor은 못 쓴다.
    with concurrent.futures.ProcessPoolExecutor(max_workers=1) as executor:
        for text_list2 in executor.map(clip_trans, aaa, timeout=60):
            print(text_list2)

    print(type(text_list2))
    for tr3 in text_list2:
        print(tr3)
    # trans_texts.append(text_list2)
    """
    tl3 = []
    print(type(trans_texts))
    for tr1 in trans_texts:
        print(tr1)
        for tr2 in tr1:
            print(tr2)
    """

    # print(tl3)
    quit()
    """
    with open("".join([str(save_path1 / file_path.stem), "_번역.txt"]), "w", encoding="utf-8") as f:
        f.writelines(text_list2)
    """
    print("저장 완료")

    print("쓰레드 실행 완료")

    with concurrent.futures.ThreadPoolExecutor() as thread:
        for a in thread.map(writefile, a24, trans_texts):
            print(type(a))

    """
    translated = executor.map(clip_trans, text_list[0])
    print(translated)
    """
    """
    for file_path, large_texts2 in zip(a24, text_list):
        writefile(file_path, translated)
    """
    # text_list3
    """
    for excue in thread.map(writefile, a24, trans_texts):
        print(excue)
    """
    # print(large_texts)
    # aaa = [executor.submit(rotaion_file, i) for i in large_texts]

    # translated_text = executor.map(clip_trans, la_text, chunksize=2048)
    # translated_texts.append(translated_text)
    # executor.shutdown(wait=True, cancel_futures=False)
    # aaa = [rotaion_file(i) for i in large_texts]
    # concurrent.futures.wait(aaa)
    # aaa = map(rotaion_file, large_texts)

    # save_que = [executor.submit(writefile, i) for i in translated_texts]
    # concurrent.futures.as_completed(save_que)

    # concurrent.futures.wait(save_que)
    # executor.shutdown(wait=True, cancel_futures=False)

    """
    for txt_path in a24:
        print(txt_path)
        with open(txt_path, "r", encoding="utf-8") as f:
            la_text = f.readlines()

        aaa = pool.map(clip_trans, la_text)  # 전체 텍스트를 한 줄 씩 분배해서 번역함.
        # print(''.join([str(save_path1 / txt_path.stem),"_번역.txt"]))
        # quit()
        with open("".join([str(save_path1 / txt_path.stem), "_번역.txt"]), "w", encoding="utf-8") as f:
            f.writelines(aaa)
    """

    end_time = time.perf_counter()
    print(f"번역에 든 시간 : {int(round((end_time - start_time) * 1000))}ms")


"""
def readfile(txt_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        return f.readlines()
"""

"""
def rotaion_file(la_text):  # 이중 맵
    return eng.executor.map(clip_trans, la_text, chunksize=2048)
"""

"""
def writefile(single_file):
    with open("".join([str(eng.save_path1 / single_file[0].stem), "_번역.txt"]), "w", encoding="utf-8") as f:
        f.writelines(single_file[1])
"""

"""
def translate_j2k(self, src_text):  # 단문 번역 메소드 - 한번에 번역할 수 있는 텍스트 길이는 4기가 정도로 추정. 대신 그만큼 느려짐.
        return self.trans(0, src_text)
"""
# 파이썬 32비트 버전에서만 됩니다. - 이 때문에 64비트 파이썬에서 쓰려면 exe를 만들어 외부로 빼야할 듯.
# 출처
# https://github.com/HelloKS/ezTransWeb


if __name__ == "__main__":
    # multiprocessing.freeze_support()
    print("Qootrans ver.0.3 !@!번역하려는 텍스트는 utf-8으로 인코딩되었고, .txt 확장자를 가진 텍스트여야 합니다!@!")

    if len(sys.argv) == 1:
        # 인자가 없으면 실행됨.
        print("call_eztrans file_mode (원문 폴더 경로) <-이런 식으로 입력")
        main("새 폴더")  # 05/01 속도 테스트 용 - 303kb로 실험. - 15790ms - 15.79초//첫번째 시도 17269ms - 17.27초 더 늘어남.//두번째 시도 12669ms - 12.67초//세번째 시도 15357ms - 15.36초
        input()  # 코드 정지용
        sys.exit()

    else:
        # 인자가 있으면 실행.
        argv1, argv2 = sys.argv[1], sys.argv[2]
        if argv1 == "clip_mode":
            while argv2 != "exit":
                print(clip_trans(argv2))
                argv2 = input()
        elif argv1 == "file_mode":
            main(argv2)

            # todo: queue를 이용해 반환값을 방출하기.
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
