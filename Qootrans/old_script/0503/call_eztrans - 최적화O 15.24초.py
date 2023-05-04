from ctypes import WinDLL, c_char_p, c_int, c_wchar_p
from ctypes.wintypes import BOOL

import pathlib
import concurrent.futures
import time
import sys
import multiprocessing
from tqdm import tqdm
from threading import RLock


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
    global bar
    try:
        a = eng.trans(0, "".join(["|:_", text])).lstrip("|:_")
        # bar.update(1)
        return a
    except Exception as e:
        # bar.update(1)
        return str(e)


def main(a22):  # 텍스트 파일들 번역용, 텍스트 파일 목록만 전달 받도록 함.
    global bar  # tqdm을 멀티프로세싱으로 돌리기 위해 전역변수로 선언.
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
            print("번역한 텍스트가 이미 있는 것 같습니다. 덮어씁니다")
            a24 = [s for s in a24 if "\\번역한_텍스트\\" not in str(s)]

    start_time = time.perf_counter()  # 시간 재기.

    def readfile(txt_path):
        with open(txt_path, "r", encoding="utf-8") as f:
            return f.readlines()

    def writefile(txt_path, txts):
        with open("".join([str(save_path1 / txt_path.stem), "_번역.txt"]), "w", encoding="utf-8") as f:
            f.writelines(txts)

    text_list = []

    with concurrent.futures.ThreadPoolExecutor() as thread:
        for large_texts in thread.map(readfile, a24):  # 멀티쓰레드를 사용하여 파일 입출력을 빠르게 함.
            text_list.append(large_texts)

    print("파일 읽기 완료")
    print(type(text_list))
    # aaa = list(text_list[0])
    futures_list = []
    bar = tqdm(total=len(text_list[0]))
    # (ProcessPoolExecutor)을 못 쓴다. eztarans J2KEngine.dll이 락이 걸려서 그런 것 같다. - 그건 틀렸다. 오류 해결. dll문제 아님. wait를 잘못 쓰고 있었다.
    """
    https://github.com/tqdm/tqdm/blob/master/examples/parallel_bars.py - 참고
    tqdm.set_lock(RLock())
    p = Pool(initializer=tqdm.set_lock, initargs=(tqdm.get_lock(),))
    p.map(partial(progresser, progress=True), L)
    
    tqdm.set_lock(RLock())
    with multiprocessing.Pool(initializer=tqdm.set_lock, initargs=(tqdm.get_lock(),)) as pool:
        # bar = tqdm(total=len(text_list[0]))
        trans_texts = pool.map(clip_trans, text_list[0])

        print("번역 완료")

        with open("".join([str(save_path1 / a24[0].stem), "_번역.txt"]), "w", encoding="utf-8") as f:
            # [s.result() for s in text_list2]
            f.writelines(trans_texts)
    """
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as thread:
        trans_texts = thread.map(clip_trans, text_list[0])
    """
    with multiprocessing.Pool() as pool:
        with concurrent.futures.ThreadPoolExecutor() as thread:
            # bar = tqdm(total=len(text_list[0]))
            trans_texts = []
            for texts, file_path in zip(text_list, a24):
                # trans_texts.append(pool.map(clip_trans, texts))
                # trans_text = pool.map(clip_trans, texts)
                thread.submit(writefile, file_path, pool.map(clip_trans, texts))

    print("번역 완료")
    # ThreadPoolExecutor(max_workers=1)로 번역했을 경우 - 54013ms - 54초
    # ThreadPoolExecutor(max_workers=4)로 번역했을 경우 - 13485ms - 13.5초
    # ThreadPoolExecutor(max_workers=6)로 번역했을 경우 - 10286ms - 10초 - 최적값
    # ThreadPoolExecutor(max_workers=8)로 번역했을 경우 - 12022ms - 12초
    # ThreadPoolExecutor(max_workers=12)로 번역했을 경우 - 19969ms - 20초
    # ThreadPoolExecutor(max_workers=16)로 번역했을 경우 - 26469ms  - 26초
    # multiprocessing.Pool()로 번역했을 경우 - 6517ms - 6.5초 - 최적값
    # multiprocessing.Pool(4)로 번역했을 경우 - 11151ms - 11초

    """
    for re in trans_texts:
        print(re)
    """
    end_time = time.perf_counter()
    print(f"번역에 든 시간 : {int(round((end_time - start_time) * 1000))}ms")


# 파이썬 32비트 버전에서만 됩니다. - 이 때문에 64비트 파이썬에서 쓰려면 exe를 만들어 외부로 빼야할 듯.
# 출처
# https://github.com/HelloKS/ezTransWeb


if __name__ == "__main__":
    multiprocessing.freeze_support()
    print("Qootrans ver.0.3 !@!번역할 텍스트는 utf-8 인코딩, .txt 확장자여야 합니다!@!")

    if len(sys.argv) == 1:
        # 인자가 없으면 실행됨.
        print("call_eztrans file_mode (원문 폴더 경로) <-이런 식으로 입력")
        main("새 폴더")  # 05/01 속도 테스트 용 - 303kb로 실험. - 15790ms - 15.79초// 05/03 - 15242ms - 15.24초
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
